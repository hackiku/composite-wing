     var points = getLookupTable(aerofoilTable, definition.aerofoil);
            var start = size(points);
    
                            
            //pull all the x-ordinates into an array
            var xArray is array = [];
            
            for (var i = 0; i < size(points); i += 1)
            {
                xArray = append(xArray, points[i][0]);
            }
            
            //This fixes a special case where some coordinate files dont have a 0,0 coordinate, this uses the minimum x value as the 0,0 ordinate
            var zeroVector is Vector = points[argMin(xArray)];
            
            //This splits the data into upper and lower 
            //This inefficiently happens even if only a single spline is required, future release should put the entire block in an if statement
            //for 'definition.noSplines == generationType.TWIN'            

            for (var i = 0; i < size(points); i += 1)
            {
                /**
                 * Moving this section of the code to the twin part breaks it because of the following line, We can either pull it into
                 * a new loop or jus keep it here. I feel it doesn't make sence evaluating if it is twin type each time. Another option
                 * could be to loop and have one if statement containing the others to reduce the number of statements we loop on.
                 * **/
                points[i] = points[i]*Cl;
                if ((definition.noSplines == generationType.TWIN) && points[i] == zeroVector*Cl)
                {
                    start = i;
                }
                if ((definition.noSplines == generationType.TWIN) && (i<=start))
                {
                    pointsUpper = append(pointsUpper, points[i]);
                }
                if ((definition.noSplines == generationType.TWIN) && (i>=start))
                {
                    pointsLower = append(pointsLower, points[i]);
                }
            }        /***-------------------------------------------------Start of Code for one Spline------------------------------------------------***/
            //Creates a closed spline for points if closed TE or a single spline with open end otherwise
            