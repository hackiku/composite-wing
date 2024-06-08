FeatureScript 608;
import(path : "onshape/std/geometry.fs", version : "608.0");
import(path:"595c85ba951f303c2032d9c4/309147ceb3195f716e224949/c6b8188181f340be01627764",version:"c4628aea4c65a27ed9733969");

export function nacaDistribution(context is Context, id is Id, debug is array, keyPoints is array, accuracy is number)
{
    /**
     * NACA Distribution uses Key Points leadind edge (normally zero), trailing edge (normally 1) and the max camber point
     * somewhere between the two. It uses these to dynamically produce an accurate point distribution at minimum cost to
     * compute time, at the moment a user can udjust how much accuracy they want however in the future they will have advance
     * options to adjust distribution magnitudes (5 magnitudes ranging from -10 to +10)
     * **/
     
     /**
      * This code isnt really suitable for LE and TE values other than 0 and 1 at the moment should I need to in the future 
      * This could be improved but since this is currently only used for naca distribution it serves its purpose.
      * **/
     
     //Check there are 3 keypoints before processing anything
    if (size(keyPoints) != 3)
    {
        throw regenError("Expecting 3 keypoints, the max camber point bound by the upper and lower bounds");
    }
    
    //Ensure the correct order is passed
    if (!(keyPoints[1] > keyPoints[0]) || !(keyPoints[1] < keyPoints[2]))
    {
        throw regenError("middle key point needs to be within the boundaries");
    }
    
    //first ordinate is the start point plus accuracy
    var x_Ordinate is number = keyPoints[0] + accuracy;
    var x_Ordinates is array = [];
    var increase is number = 0;
    
    //if in debug mode read out what has been passed as accuracy
    if (debug[0] != undefined)
        {
            if (isIn('distribRead', debug[0]) == true)
            {
                println("Distribution Debug:");
                
                print("Passed accuracy = ");
                println(accuracy);
            }
        }
    
    //start by appending zero point as this is always required
    x_Ordinates = append(x_Ordinates, 0);
    
    
    while (x_Ordinate < 1)
    {
        //append ordinate (first itteration will be the initial x ordinate)
        x_Ordinates = append(x_Ordinates, x_Ordinate);
        
        //condition between LE and 1/3 max camber
        if (x_Ordinate < keyPoints[1]/3)
        {
            increase = increase + accuracy*2;
            
            if (increase < accuracy)
            {
                increase = accuracy;
            }
        }
        //condition between 1/3 max thickness and 2/3 max thickness
        else if ((x_Ordinate > keyPoints[1]/3) && (x_Ordinate < 2*(keyPoints[1]/3)))
        {
            increase = increase + accuracy*4;
            
            if (increase < accuracy)
            {
                increase = accuracy;
            }
        }
        //condition between 2/3 max thickness and max thickness
        else if ((x_Ordinate > 2*(keyPoints[1]/3)) && (x_Ordinate < keyPoints[1]))
        {
            increase = increase - accuracy;
            
            if (increase < accuracy)
            {
                increase = accuracy;
            }
        }
        //condition between max thickness and half way between max thick and TE
        //0.75 of of final point is not good, it doesnt dynamically change. Should be addressed in future update
        else if ((x_Ordinate > keyPoints[1]) && (x_Ordinate < 0.75*(keyPoints[2])))
        {
            increase = increase + 2*accuracy;
            
            if (increase < accuracy)
            {
                increase = accuracy;
            }
        }
        //condition for the last section
        else
        {
            increase = increase - 5*accuracy;
            
            if (increase < accuracy)
            {
                increase = accuracy;
            }
        }
        
        //Add the increase to the current x ordinate
        x_Ordinate = x_Ordinate + increase;
        
        /**----------------------------------------------------Integrated Debug Code Start------------------------------------------**/
        //print all x values iteratively
        if (debug[0] != undefined)
        {
            if (isIn('distribRead', debug[0]) == true)
            {
                println(x_Ordinate);
            }
        }
        /**----------------------------------------------------Integrated Debug Code End------------------------------------------**/
    }
    
    //at the end append the last ordinate of 1
    if (x_Ordinates[size(x_Ordinates)-1] != 0)
    {
        x_Ordinates = append(x_Ordinates, 1);
    }
    
    //If in debug mode print number of ordinates in the final distribution
    if (debug[0] != undefined)
    {
        if (isIn('distribRead', debug[0]) == true)
        {
            print("Distribution Size = ");
            println(size(x_Ordinates));
        }
    }
    
    return x_Ordinates;
}


export function NACA(context is Context, id is Id, noDigits is number, x_Ordinates is array, digits is array, Cl is ValueWithUnits, TE is string, debug is array)
{
    /**
     * NACA function currently supports four digits with the intention of supporting 5 digits in the future, and it produces
     * closed trailing edge, although it has the infastructure for open it is untested and unused.
     * **/
     
    //Ensue that only 4 digits can be used
    if (noDigits !=4)
    {
        throw regenError("NACA function only currently supports NACA 4 Digit parametric Aerofoils");
    }
    
    //Ensure that only closed edges can be used
    if (TE == 'open')
    {
        throw regenError("NACA function only currently supports closed trailing edges");
    }
    //Define the 'a' coeficients
    const a0=1.4845; const a1=0.6300; const a2=1.7580; const a3=1.4215; var a4=0;
    
    //Define the 'c' coeficients
    const c1=digits[0]/(digits[1])^2;
    const c2=digits[0]/(1-digits[1])^2;
    
    //define the 'y' ordinate variables for camber and thickness
    var yc=[]; var yt=[];
    
    //Define the arrays holding the output points
    var pointsCamber=[]; var pointsUpper=[]; var pointsLower=[];
    
    //Evaluate weather the trailing edge is open or closed
    if (TE == 'closed')
    {
        a4=0.518;
    }
    else
    {
        a4=0.5075;
    }
    
    //Run each 'x' ordinate through the naca equations
    for (var x_Ordinate in x_Ordinates)
    {
        //Ensure that if 'x' = 0 that all y values are 0 (not just close too, this was done because of numerical errors
        if (x_Ordinate==0)
        {
            yc=0; yt=0; 
        }
        //If 'x' ordinate is smaller than max camber
        if (x_Ordinate>0 && x_Ordinate<digits[1])
        {
            yc=c1*((2*digits[1]*x_Ordinate)-x_Ordinate^2);
            yt=digits[2]*(a0*(x_Ordinate^0.5)-a1*x_Ordinate-a2*(x_Ordinate^2)+a3*(x_Ordinate^3)-a4*(x_Ordinate^4));
        }
        //If 'x' ordinate is bigger than max camber
        if (x_Ordinate>=digits[1])
        {
            yc=c2*(((1)-(2*digits[1]))+(2*digits[1]*x_Ordinate)-x_Ordinate^2);
            yt=digits[2]*(a0*(x_Ordinate^0.5)-a1*x_Ordinate-a2*(x_Ordinate^2)+a3*(x_Ordinate^3)-a4*(x_Ordinate^4));
        }
        
        //allow debuging of all points
        if (debug[0] != undefined)
        {
            if (isIn('nacaPoints', debug[0]) == true)
            {
                debug(context, planeToWorld(debug[1], vector(Cl*x_Ordinate,yc*Cl)));
                debug(context, planeToWorld(debug[1], vector(Cl*x_Ordinate,(yc+yt)*Cl)));
                debug(context, planeToWorld(debug[1], vector(Cl*x_Ordinate,(yc-yt)*Cl)));
            }
        }
        pointsCamber=append(pointsCamber, vector(Cl*x_Ordinate,yc*Cl));
        pointsUpper=append(pointsUpper, vector(Cl*x_Ordinate,(yc+yt)*Cl));
        pointsLower=append(pointsLower, vector(Cl*x_Ordinate,(yc-yt)*Cl));
    }
    
    //print all coeficients
    if (debug[0] != undefined)
    {
        if (isIn('nacaCoefs', debug[0]) == true)
        {
            print('c1: ');
            print(c1);
            print('c2: ');
            println(c2);
            
            print('a0: ');
            print(a0);
            print('a1: ');
            print(a1);
            print('a2: ');
            print(a2);
            print('a3: ');
            print(a3);
            print('a4: ');
            println(a4);
        }
    }
    
    var pointMap is map = {'Camber' : pointsCamber, 'Upper' : pointsUpper, 'Lower' : pointsLower};
    
    return pointMap;
}