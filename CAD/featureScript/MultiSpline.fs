FeatureScript 2368;
import(path : "onshape/std/common.fs", version : "2368.0");

annotation { "Feature Type Name" : "Airfoil Smoothie" }
export const multiSpline = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        //Select Aerofoils to join
        annotation { "Name" : "Sketch Profile", "Filter" : EntityType.FACE }
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
        var ElapsedTime = 'Elapsed Time';
        startTimer(ElapsedTime);
        var Loft_Profiles = [];
        var foils = size(evaluateQuery(context, qEntityFilter(definition.sketchProfile, EntityType.FACE)));
        var noPoints = 0;
        var digit = definition.Accuracy;
        
        var UpperCurves = [];
        var LowerCurves = [];
        
        var Map = {}; //IMPORTANT: Define Map to put points for each aerofoil into

        // Outer loop for each airfoil
        for (var a = 1; a <= foils; a += 1)
        {
            // Select aerofoil
            var profile = qNthElement(definition.sketchProfile, a-1);
            
            // Query upper and lower edges
            var lines = qEdgeAdjacent(qEntityFilter(profile, EntityType.FACE), EntityType.EDGE);
            var noLines = evaluateQuery(context, lines);
            var points = [];

            // Define upperPoints array
            var upperPoints = [];

            print('Number of lines: ');
            println(size(noLines));
            
            // Loop for each line
            for (var L = 0; L <= size(noLines) - 1; L += 1)
            {
                var line = qNthElement(lines, L);
                
                // Inner loop for each point
                for (var k = digit; k < 0.999; k += digit)
                {
                    // Use the origin of the tangent line as point
                    var Tangents1 = evEdgeTangentLine(context, {
                        "edge" : line,
                        "parameter" : k,
                        "arcLengthParameterization" : false
                    });
                    var point = Tangents1.origin;
                    
                    // Classify and append points to upperPoints
                    if (point[1] > 0) // TODO
                    {
                        upperPoints = append(upperPoints, point);
                    }
                    
                    points = append(points, point);
                    noPoints = noPoints + 1;
                }
            }

            // Append adjacent vertex points if LTG is true
            if (definition.LTG == true)
            {
                var LTPoints = qVertexAdjacent(qEntityFilter(profile, EntityType.FACE), EntityType.VERTEX);
                var noLTPoints = size(evaluateQuery(context, LTPoints));
                
                print('Adding Adjacent Points, Number of points = ');
                println(noLTPoints);
                
                for (var LT = 0; LT < noLTPoints; LT += 1)
                {
                    var LTPoint = evVertexPoint(context, {
                        "vertex" : qNthElement(LTPoints, LT)
                    });
                    points = append(points, LTPoint);
                }
            }
            
            // Store the points in the map and loft profiles
            Map[a] = points;
            Loft_Profiles = append(Loft_Profiles, profile);
            
            // Print upperPoints array for debugging
            print("Upper Points for airfoil " + toString(a) + ": ");
            println(upperPoints);
        }
        
        // Optional: Run a loft between the identical points on all profiles
        if (definition.Loft == true)
        {
            var Guides = [];
            
            for (var y = 0; y <= size(Map[1]) - 1; y += 1)
            {
                var arraySpline = [];
                for (var x = 1; x <= foils; x += 1)
                {
                    arraySpline = append(arraySpline, Map[x][y]);
                }
                opFitSpline(context, id + "3DSpline" + y, {
                    "points" : arraySpline
                });
                Guides = append(Guides, qCreatedBy(id + "3DSpline" + y, EntityType.EDGE));
            }
            
            opLoft(context, id + "AerofoilLoft", {
                "profileSubqueries" : Loft_Profiles,
                "guideSubqueries" : Guides
            });
        }
        
        // Print elapsed time for debugging
        print('End Time:\t\t');
        printTimer(ElapsedTime);
    });

const RealBounds = {
    (unitless) : [0.001, 0.1, 0.5]
} as RealBoundSpec;
