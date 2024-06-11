
FeatureScript 2368;
import(path : "onshape/std/common.fs", version : "2368.0");
import(path : "onshape/std/geometry.fs", version : "442.0");


annotation { "Feature Type Name" : "Airfoil Smoothie v2" }
export const multiSpline = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        //Select Aerofoils to join
        annotation { "Name" : "Sketch Profile", "Filter" : EntityType.FACE}
        definition.sketchProfile is Query;
        
        annotation { "Name" : "Include LE and TE Guides?" }
        definition.LTG is boolean;
        
        annotation { "Name" : "Accuracy (Between 1e-3 and 0.5)" }
        isReal(definition.Accuracy, RealBounds);
        
        annotation { "Name" : "Loft Between Aerofoils?" }
        definition.Loft is boolean;

        annotation { "Name" : "Show Lines?" }
        definition.showLines is boolean;        
    }
    {
        var ElapsedTime = 'Ellapsed Time';
        startTimer(ElapsedTime);
        var Loft_Profiles = [];
        var foils = size(evaluateQuery(context, qEntityFilter(definition.sketchProfile, EntityType.FACE)));
        var noPoints = 0;
        var digit = definition.Accuracy;
        var noLTPoints = 0;
        var LineItter = 0;
        var Map = {};//IMPORTANT: Define Map to put points for each aerofoil into
        
        
        //outer loop for each aerofoil
        for (var a = 1; a <= foils; a += 1)
        {
            //select aerofoil
            var profile = qNthElement(definition.sketchProfile, a-1);
            //debug(context, profile);
            
            //query upper and lower edges
            var lines = qEdgeAdjacent(qEntityFilter(profile, EntityType.FACE), EntityType.EDGE);
            var noLines = evaluateQuery(context, lines);
            var points = [];
            
            //This line isnt an error: DO NOT DELETE. Using profile didn't resolve in 2 vertex's
            var LTPoints = qVertexAdjacent(qEntityFilter(qNthElement(definition.sketchProfile, a-1), EntityType.FACE), EntityType.VERTEX);
            
            
            //print('No of lines:');
            //println(size(noLines));
            
            //Loop for each line
            for (var L = 0; L <= size(noLines)-1; L += 1)
            {
                    //seperate the lines into different variables
                    var line = qNthElement(lines, L);
                    
                    //inner loop for each point
                    for (var k = digit; k < 0.999; k += digit)
                    //0.999 to stop 0.99999999999 being allowed because of computational inaccuracys
                        {
                            //print('Aerofoil Iterations = ');
                            //print(a);
                            //print('\t\tLine Iterations = ');
                            //print(L+1);
                            //print('\tPoint Iterations = ');
                            //print(k);
                            //print('\t');
                            
                            
                            
                            
                            //use the origin of tangent line as point
                            var Tangents1 = evEdgeTangentLine(context, {
                                "edge" : line,
                                "parameter" : k,
                                "arcLengthParameterization" : false
                            });
                            var point = Tangents1.origin;
                            
                            
                            
                            
                            points = append(points, point);
                            noPoints = noPoints+1;
                            
                            //print('\tPoint Number\t');
                            //print(noPoints);
                            //print('\t');
                            //printTimer(ElapsedTime);
                        }
            
            }
            //Append adjacent vertexes here?
            if (definition.LTG == true)
            {
                print('Adding Adjacent Points, Number of points = ');
                println(noLTPoints);
                
                noLTPoints = size(evaluateQuery(context, LTPoints));
                for (var LT = 0; LT < noLTPoints; LT += 1)
                {
                    var LTPoint = [];
                    LTPoint = evVertexPoint(context, {
                    "vertex" : qNthElement(LTPoints, LT)
                });
                points = append(points, LTPoint);
                }
                
                
            }
            LineItter = size(points);
            //println(LineItter);
            
            Map[a]=points;
            Loft_Profiles = append(Loft_Profiles, profile);
        } 
        //print('End of point iterations, total number of points =');
        //println(noPoints);
        
        /**Run a loft between the identical points on all profiles **/
        var Guides = [];
        
        //println('Line Array Iteratons:\n');
        for (var y = 0; y <= LineItter-1; y += 1)
        {
            var arraySpline = [];
            var IterationArray = [];
            
            for (var x = 1; x <= foils; x += 1)
            {
                IterationArray = Map[x];
                arraySpline = append(arraySpline, IterationArray[y]);
                //print('\nLine Number = ');
                //print(y+1);
                //print('\t\tPoint Number = ');
                //print(x);
                //print('\t');
                //printTimer(ElapsedTime);
            }
            opFitSpline(context, id + "3DSpline" + y, {
                    "points" : arraySpline
            
                });
            
            Guides = append(Guides, qCreatedBy(id + "3DSpline" + y, EntityType.EDGE));
        }
        //print('Total Number of Guides');
        //println(size(Guides));
        
        /**If the user is lofting between the profiles using the quides without any post processing
         * then they would be better of being able to loft within the feature, removing any unnecessary
         * repition**/
         
        if (definition.Loft == true)
        {
            opLoft(context, id + "AerofoilLoft", {
                    "profileSubqueries" : Loft_Profiles,
                    "guideSubqueries" : Guides
            });
            //print(getFeatureError(context, id + "AerofoilLoft"));
        }
        //print('End Time:\t\t');
        //printTimer(ElapsedTime);
        
            
    });
    const RealBounds = {
                            (unitless) : [0.001,0.1,0.5]
                        } as RealBoundSpec;
