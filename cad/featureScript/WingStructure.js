FeatureScript 559;
import(path : "onshape/std/geometry.fs", version : "559.0");

export enum topTab
{
    annotation { "Name" : "Ribs" }
    RIBS,
    annotation { "Name" : "Stifeners" }
    STIFF,
}

export enum ribTab
{
    annotation { "Name" : "Add" }
    ADD,
    /*
    annotation { "Name" : "Lighten" }
    LIGHT,
    annotation { "Name" : "Shape" }
    SHAPE
    */
}

export enum addRibTab
{
    annotation { "Name" : "Add on Plane" }
    ONPLANE,
    annotation { "Name" : "Multi-Rib" }
    MULTIRIB,
    
}

export enum stiffTab
{
    annotation { "Name" : "Spar from Position" }
    SPARPOS,
    annotation { "Name" : "Spar on Plane" }
    SPARPLANE,
    annotation { "Name" : "Stringer" }
    STRINGER
}


export enum sparType
{
    annotation { "Name" : "Solid" }
    SOLID,
    annotation { "Name" : "I-Beam" }
    IBEAM,
    annotation { "Name" : "Box" }
    BOX
    
}

export enum stringerType
{
    annotation { "Name" : "Solid" }
    SOLID,
    annotation { "Name" : "Tubular" }
    TUBE,
    
}
/**
export function rememberMe_Plane(rem)
{
    if (rem == true)
    {
        return { "Name" : "Select Plane", "Filter" : EntityType.FACE, "MaxNumberOfPicks" : 1, "UIHint" : "REMEMBER_PREVIOUS_VALUE"};
    }
    if (rem == false)
    {
        return { "Name" : "Select Plane", "Filter" : EntityType.FACE, "MaxNumberOfPicks" : 1 };
    }
}
**/

annotation { "Feature Type Name" : "Wing Structure" }
export const WingStructure = defineFeature(function(context is Context, id is Id, definition is map)
    precondition
    {
        annotation { "Name" : "Tab", "UIHint" : "HORIZONTAL_ENUM" }
        definition.topTab is topTab;
        
        //annotation { "Name" : "Remember Previous Selection" }
        //definition.previous is boolean;
        
        annotation { "Name" : "Select Plane", "Filter" : EntityType.FACE, "MaxNumberOfPicks" : 1, "UIHint" : "REMEMBER_PREVIOUS_VALUE" }
        definition.selectPlane is Query;
        
        annotation { "Name" : "Select Wing", "Filter" : EntityType.BODY, "MaxNumberOfPicks" : 1, "UIHint" : "REMEMBER_PREVIOUS_VALUE" }
        definition.wing is Query;
        
        annotation { "Name" : "Select [LE-Base, TE-Base, TE-Tip, LE-Tip]", "Filter" : EntityType.VERTEX, "MaxNumberOfPicks" : 4, "UIHint" : "REMEMBER_PREVIOUS_VALUE" }
        definition.points is Query;
        
        if (definition.topTab == topTab.RIBS)
        {
            annotation { "Name" : "Tab", "UIHint" : "HORIZONTAL_ENUM" }
            definition.ribTab is ribTab;
            
            if (definition.ribTab == ribTab.ADD)
            {
                annotation { "Name" : "Rib Width" }
                isLength(definition.ribWidth, LENGTH_BOUNDS);
                
                annotation { "Name" : "Flip", "UIHint" : "OPPOSITE_DIRECTION" }
                definition.flip2 is boolean;
                
                annotation { "Name" : "Add Ribs", "UIHint" : "HORIZONTAL_ENUM" }
                definition.addRibTab is addRibTab;
                
                if (definition.addRibTab == addRibTab.ONPLANE)
                {
                    annotation { "Name" : "Face Plane", "Filter" : EntityType.FACE, "MaxNumberOfPicks" : 1 }
                    definition.ribPlane is Query;
                    
                    annotation { "Name" : "Offset" }
                    isLength(definition.offSet1, OFFSET_BOUNDS);
                    
                }
                if (definition.addRibTab == addRibTab.MULTIRIB)
                {
                    annotation { "Name" : "Number of Ribs" }
                    isInteger(definition.noRibs, POSITIVE_COUNT_BOUNDS);
                }
            }
        }
        
        
        if (definition.topTab == topTab.STIFF)
        {
            annotation { "Name" : "Tab", "UIHint" : "HORIZONTAL_ENUM" }
            definition.stiffTab is stiffTab;
            
            if ((definition.stiffTab == stiffTab.SPARPOS) || (definition.stiffTab == stiffTab.SPARPLANE))
            {
                if (definition.stiffTab == stiffTab.SPARPLANE)
                {
                    annotation { "Name" : "Select Spar Plane", "Filter" : EntityType.FACE&&GeometryType.PLANE, "MaxNumberOfPicks" : 1 }
                    definition.sparPlane is Query;
                }
                
                annotation { "Name" : "Spar Width" }
                isLength(definition.sparWidth, LENGTH_BOUNDS);
                
                if (definition.stiffTab == stiffTab.SPARPLANE)
                {
                    annotation { "Name" : "Flip", "UIHint" : "OPPOSITE_DIRECTION" }
                    definition.flip is boolean;
                }
                
                annotation { "Name" : "Spar Type" }
                definition.sparType is sparType;
                
                if (definition.sparType == sparType.IBEAM)
                {
                    annotation { "Name" : "Wall Thickness" }
                    isLength(definition.ibeamWall, WALL_THICK_BOUNDS);
                }
                if (definition.sparType == sparType.BOX)
                {
                    annotation { "Name" : "Outer Radius" }
                    isLength(definition.filletRad, WALL_THICK_BOUNDS);
                    
                    annotation { "Name" : "Wall Thickness" }
                    isLength(definition.boxWall, WALL_THICK_BOUNDS);
                }
            }
            
            
            
            if (definition.stiffTab == stiffTab.STRINGER)
            {
                annotation { "Name" : "Stringer Type" }
                definition.stringerType is stringerType;
                
                annotation { "Name" : "Outer Diameter" }
                isLength(definition.outerDia, LENGTH_BOUNDS);
                
                if (definition.stringerType == stringerType.TUBE)
                {
                    annotation { "Name" : "Wall Thickness" }
                    isLength(definition.stringerWall, LENGTH_BOUNDS);
                }
            }
            
        
            if ((definition.stiffTab == stiffTab.SPARPOS)||(definition.stiffTab == stiffTab.STRINGER))
            {
                annotation { "Name" : "Horizontal Base Position" }
                isReal(definition.basePos, POS_BOUNDS);
                
                annotation { "Name" : "Horizontal Tip Position" }
                isReal(definition.tipPos, POS_BOUNDS);
            }
            if (definition.stiffTab == stiffTab.STRINGER)
            {
                annotation { "Name" : "Vertical Base Position" }
                isReal(definition.VertBasePos, POS_BOUNDS);
                
                annotation { "Name" : "Vertical Tip Position" }
                isReal(definition.VertTipPos, POS_BOUNDS);
            }
        }
    }   
    {
        var rawPoints = evaluateQuery(context, definition.points);
        var points = {};
        
        //plane used for the normal of EVERY operation
        var centerPlane = evFaceTangentPlane(context, {
                "face" : definition.selectPlane,
                "parameter" : vector(0.5, 0.5)
            });
        
        
        transform(context, id +"transform", {
                "entities" : qOwnerBody(definition.wing),
                "transformType" : TransformType.COPY,
                "dx" : 0 * inch,
                "dy" : 0 * inch,
                "dz" : 0 * inch,
                "makeCopy" : true
        });
        
        
        /**Create a map of points to be used for calculating later parameters, if however, the user
        Doesn't define enough point throw an error to prevent default, non descriptive error.   **/
        if (size(rawPoints) == 4)
        {
            //points and maps
            points = {"LE-Base": evVertexPoint(context, {"vertex" : rawPoints[0]}),
                        "TE-Base": evVertexPoint(context, {"vertex" : rawPoints[1]}),
                        "TE-Tip": evVertexPoint(context, {"vertex" : rawPoints[2]}),
                        "LE-Tip": evVertexPoint(context, {"vertex" : rawPoints[3]})
            };
        }
        else
        {
            //error to be thrown
            throw regenError("Error: Not enough points are defined");
        }
        
        //the normal of that plane    
        var normal = centerPlane.normal;
        
        var planeDirect = points["LE-Base"] - points["TE-Base"];
        var planeTipDirect = points["LE-Base"] - points["TE-Base"];
        
        var verticalDirect = cross(normal, planeDirect);
        var verticalTipDirect = cross(normal, planeTipDirect);
        
        //Evaluate the cord length of both the base and tip
        var baseDirect = points["LE-Base"]-points["TE-Base"];
        var tipDirect = points["LE-Tip"]-points["TE-Tip"];
        
        var baseCord = evDistance(context, {
                "side0" : points["LE-Base"],
                "side1" : points["TE-Base"]
        }).distance;
        
        var tipCord = evDistance(context, {
                "side0" : points["LE-Tip"],
                "side1" : points["TE-Tip"]
        }).distance;
        
        var baseNorm = -baseDirect/baseCord;
        var tipNorm = -tipDirect/tipCord;
        
        var basePlane = opPlane(context, id + "basePlane", {
                "plane" : plane(points["LE-Base"], cross(baseNorm, verticalDirect), baseDirect),
                "width" : baseCord ,
                "height" : 0.1*baseCord
        });
        var tipPlane = opPlane(context, id + "tipPlane", {
                "plane" : plane(points["LE-Tip"], cross(tipNorm, verticalDirect), tipDirect),
                "width" : baseCord ,
                "height" : 0.1*baseCord
        });
        
        var solid = qCreatedBy(id +"transform", EntityType.BODY);
        
        try silent
        {
            opSplitPart(context, id + "BaseSplit", {
                    "targets" : solid,
                    "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "basePlane"), EntityType.FACE))
            });
            println("Base Split successful");
        }
        try silent
        {
            opSplitPart(context, id + "tipSplit", {
                    "targets" : solid,
                    "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "tipPlane"), EntityType.FACE))
            });
            println("Tip Split successful");
        }
        
        solid = qIntersectsPlane(qOwnerBody(solid), plane((points["LE-Tip"]+points["TE-Base"])/2, normal));
        try silent
        {
            opDeleteBodies(context, id + "HighLevelDelete", {
                "entities" : qSubtraction(qOwnedByBody(qCreatedBy(id +"transform"), EntityType.BODY), solid)
            });
        }
        
        /**-----------------------------------------------------Start of Main Code-------------------------------------------------**/
        if (definition.topTab == topTab.RIBS)
        {
            /**--------------------------------------------------Start of Rib Code-------------------------------------------------**/
            var plane1 is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                var plane2 is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                
                var basePoint is Vector = vector(0, 0, 0);
                var ribNorm is Vector = vector(0, 0, 0);
                var ribPlanex is Vector = vector(0, 0, 0);
            
            if (definition.addRibTab == addRibTab.ONPLANE)
            {
                /**------------------------------------------Start of Rib on plane Code--------------------------------------------**/
                ribNorm = evFaceTangentPlane(context, {
                                    "face" : definition.ribPlane,
                                    "parameter" : vector(0.5, 0.5)
                                    }).normal;
                
                var planeCentre = evApproximateCentroid(context, {
                                    "entities" : definition.ribPlane
                                    });
                
                
                
                if (definition.flip2 == false)
                {
                    plane1 = plane((planeCentre + ribNorm*definition.offSet1), ribNorm);
                    plane2 = plane((planeCentre + ribNorm*definition.offSet1 + ribNorm*definition.ribWidth), ribNorm);
                    basePoint = planeCentre + ribNorm*definition.offSet1 + ribNorm*definition.ribWidth/2;
                }
                else
                {
                    plane1 = plane((planeCentre - ribNorm*definition.offSet1), ribNorm);
                    plane2 = plane((planeCentre - ribNorm*definition.offSet1 - ribNorm*definition.ribWidth), ribNorm);
                    basePoint = planeCentre - ribNorm*definition.offSet1 - ribNorm*definition.ribWidth/2;
                }
                var ribPlane1 = opPlane(context, id + "ribPlane1", {
                                "plane" : plane1,
                                "width" : baseCord ,
                                "height" : 0.1*baseCord
                                });
                                
                var ribPlane2 = opPlane(context, id + "ribPlane2", {
                                "plane" : plane2,
                                "width" : baseCord ,
                                "height" : 0.1*baseCord
                                });
                
                opSplitPart(context, id + "ribSplit1", {
                    "targets" : solid,
                    "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "ribPlane1"), EntityType.FACE))
                    });
                    
                solid = qOwnedByBody(qCreatedBy(id +"transform", EntityType.BODY), EntityType.BODY);
                
                opSplitPart(context, id + "ribSplit2", {
                    "targets" : solid,
                    "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "ribPlane2"), EntityType.FACE))
                    });
                
                solid = qOwnedByBody(qCreatedBy(id +"transform"), EntityType.BODY);
                
                opDeleteBodies(context, id + "deleteNonSpar", {
                        "entities" : qSubtraction(solid, qIntersectsPlane(qOwnerBody(solid), plane(basePoint, ribNorm)))
                });
                /**------------------------------------------End of Rib on plane Code----------------------------------------------**/
            }
            if (definition.addRibTab == addRibTab.MULTIRIB)
            {
                /**-------------------------------------------Start of multi Rib Code----------------------------------------------**/
                var wingLen = dot(points["TE-Tip"] - points["TE-Base"], normal);
                var wingInterval is ValueWithUnits = wingLen/(definition.noRibs+1);
                var planeCentre = (points["LE-Base"] + points["TE-Base"])/2;
                
                var plane1 is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                var plane2 is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                
                var idKey = 0;
                
                var ribPlane1 = {};
                var ribPlane2 = {};
                
                var ribQuery = [];
                
                for (var i = wingInterval; i < wingLen; i += wingInterval)
                {
                    println(idKey);
                    
                    plane1 = plane((planeCentre + (i-definition.ribWidth/2)*normal), normal);
                    plane2 = plane((planeCentre + (i+definition.ribWidth/2)*normal), normal);
                    
                    ribPlane1 = opPlane(context, id + "multiRibLoop" + idKey + "ribPlane1", {
                                    "plane" : plane1,
                                    "width" : baseCord ,
                                    "height" : 0.1*baseCord
                                    });
                    
                    ribPlane2 = opPlane(context, id + "multiRibLoop" + idKey + "ribPlane2", {
                                    "plane" : plane2,
                                    "width" : baseCord ,
                                    "height" : 0.1*baseCord
                                    });
                    
                    solid = qOwnedByBody(qCreatedBy(id +"transform", EntityType.BODY), EntityType.BODY);
                    
                    opSplitPart(context, id + "multiRibLoop" + idKey + "ribSplit1", {
                                "targets" : qIntersectsPlane(qOwnerBody(solid), plane(planeCentre + i*normal, normal)),
                                "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "multiRibLoop" + idKey + "ribPlane1"), EntityType.FACE))
                                });
                    
                    solid = qOwnedByBody(qCreatedBy(id +"transform", EntityType.BODY), EntityType.BODY);
                    
                    opSplitPart(context, id + "multiRibLoop" + idKey + "ribSplit2", {
                                "targets" : qIntersectsPlane(qOwnerBody(solid), plane(planeCentre + i*normal, normal)),
                                "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "multiRibLoop" + idKey + "ribPlane2"), EntityType.FACE))
                                });
                    
                    ribQuery = append(ribQuery, qIntersectsPlane(qOwnerBody(solid), plane(planeCentre + i*normal, normal)));
                    
                    idKey +=1;
                
                }
                ribQuery = qUnion(ribQuery);
                
                opDeleteBodies(context, id + "multiRibLoop" + idKey + "deleteNonRib", {
                                "entities" : qSubtraction(solid, ribQuery)
                                });
                /**---------------------------------------------End of multi Rib Code----------------------------------------------**/
            }
            /**---------------------------------------------------End of Rib Code--------------------------------------------------**/
        }
        if (definition.topTab == topTab.STIFF)
        {
            /**------------------------------------------------Start of Stiffner Code----------------------------------------------**/
            
            if ((definition.stiffTab == stiffTab.SPARPOS) || (definition.stiffTab == stiffTab.SPARPLANE))
            {
                
                var plane1 is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                var plane2 is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                
                var centrePlane is Plane = plane(vector(0*meter, 0*meter, 0*meter), vector(1, 0, 0), vector(0, 1, 0));
                var basePoint is Vector = vector(0, 0, 0);
                var sparNorm is Vector = vector(0, 0, 0);
                var sparPlanex is Vector = vector(0, 0, 0);
                
                if (definition.stiffTab == stiffTab.SPARPOS)
                {
                    /**--------------------------------------Start of Spar Position Code-------------------------------------------**/
                    var tipPoint = points["LE-Tip"] + definition.tipPos*tipCord*tipNorm;
                
                    basePoint = points["LE-Base"] + definition.basePos*baseCord*baseNorm;
                    
                    var sparDist = evDistance(context, {
                                    "side0" : basePoint,
                                    "side1" : tipPoint
                                    }).distance;
                                    
                    var sparDirect = basePoint - tipPoint;
                    
                    var sparPlanex = sparDirect/sparDist;
                    sparNorm = cross(verticalDirect, sparPlanex)/meter;
                    
                    centrePlane = plane(basePoint, sparNorm, sparPlanex);
                    plane1 = plane((basePoint + sparNorm*definition.sparWidth/2), sparNorm, sparPlanex);
                    plane2 = plane((basePoint - sparNorm*definition.sparWidth/2), sparNorm, sparPlanex);
                    /**---------------------------------------End of Spar Position Code--------------------------------------------**/
                }
                else
                {
                    /**----------------------------------------Start of Spar Plane Code--------------------------------------------**/
                    sparNorm = evFaceTangentPlane(context, {
                                        "face" : definition.sparPlane,
                                        "parameter" : vector(0.5, 0.5)
                                        }).normal;
                    
                    var planeCentre = evApproximateCentroid(context, {
                                        "entities" : definition.sparPlane
                                        });
                    
                    plane1 = plane((planeCentre), sparNorm);
                    
                    if (definition.flip == false)
                    {
                        plane2 = plane((planeCentre + sparNorm*definition.sparWidth), sparNorm);
                        basePoint = planeCentre + sparNorm*definition.sparWidth/2;
                    }
                    else
                    {
                        plane2 = plane((planeCentre - sparNorm*definition.sparWidth), sparNorm);
                        basePoint = planeCentre - sparNorm*definition.sparWidth/2;
                    }
                    centrePlane = plane(basePoint, sparNorm);
                    
                    /**----------------------------------------End of Spar Plane Code--------------------------------------------**/
                }
                /**----------------------------------------start of shared Spar Plane Code---------------------------------------**/
                var sparPlane1 = opPlane(context, id + "sparPlane1", {
                                "plane" : plane1,
                                "width" : baseCord ,
                                "height" : 0.1*baseCord
                                });
                                
                var sparPlane2 = opPlane(context, id + "sparPlane2", {
                                "plane" : plane2,
                                "width" : baseCord ,
                                "height" : 0.1*baseCord
                                });
                
                opSplitPart(context, id + "sparSplit1", {
                                "targets" : solid,
                                "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "sparPlane1"), EntityType.FACE))
                                });
                
                opSplitPart(context, id + "sparSplit2", {
                                "targets" : solid,
                                "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "sparPlane2"), EntityType.FACE))
                                });
                
                solid = qOwnedByBody(qCreatedBy(id +"transform"), EntityType.BODY);
                
                opDeleteBodies(context, id + "deleteNonSpar", {
                                "entities" : qSubtraction(solid, qIntersectsPlane(qOwnerBody(solid), plane(basePoint, sparNorm)))
                });
                if (definition.sparType == sparType.IBEAM)
                {
                    /**----------------------------------------start of I-Beam Spar Plane Code-----------------------------------**/
                    var sparPlane2 = opPlane(context, id + "centrePlane", {
                                "plane" : centrePlane,
                                "width" : baseCord ,
                                "height" : 0.1*baseCord
                                });
                    
                    opSplitPart(context, id + "splitSpar", {
                                "targets" : solid,
                                "tool" : qOwnerBody(qEntityFilter(qCreatedBy(id + "centrePlane"), EntityType.FACE))
                                });
                    
                    var sideFaces = qUnion([qCoincidesWithPlane(qOwnedByBody(solid, EntityType.FACE), plane1),qCoincidesWithPlane(qOwnedByBody(solid, EntityType.FACE), plane2), qCoincidesWithPlane(qOwnedByBody(solid, EntityType.FACE), plane(points["LE-Base"], cross(baseNorm, verticalDirect), baseDirect)), qCoincidesWithPlane(qOwnedByBody(solid, EntityType.FACE), plane(points["LE-Tip"], cross(tipNorm, verticalDirect), tipDirect))]);
                    
                    opShell(context, id + "shell1", {
                                "entities" : qUnion([solid, sideFaces]),
                                "thickness" : -definition.ibeamWall
                                });
                    
                    opBoolean(context, id + "rejoinBeam", {
                                "tools" : solid,
                                "operationType" : BooleanOperationType.UNION
                                });
                    /**----------------------------------------End of I-Beam Spar Plane Code-------------------------------------**/
                }
                if (definition.sparType == sparType.BOX)
                {
                    /**-----------------------------------------Start of Box Spar Plane Code-------------------------------------**/
                    var sideFaces is Query = qNothing();
                    var allEdges is Query = qNothing();
                    var nonEdges is Query = qNothing();
                    
                    sideFaces = qUnion([qCoincidesWithPlane(qOwnedByBody(solid, EntityType.FACE), plane(points["LE-Base"], cross(baseNorm, verticalDirect), baseDirect)), qCoincidesWithPlane(qOwnedByBody(solid, EntityType.FACE), plane(points["LE-Tip"], cross(tipNorm, verticalDirect), tipDirect))]);
                    
                    allEdges = qUnion([qCoincidesWithPlane(qOwnedByBody(solid, EntityType.EDGE), plane1),qCoincidesWithPlane(qOwnedByBody(solid, EntityType.EDGE), plane2)]);
                    
                    nonEdges = qUnion([qCoincidesWithPlane(qOwnedByBody(solid, EntityType.EDGE), plane(points["LE-Base"], cross(baseNorm, verticalDirect), baseDirect)), qCoincidesWithPlane(qOwnedByBody(solid, EntityType.EDGE), plane(points["LE-Tip"], cross(tipNorm, verticalDirect), tipDirect))]);
                    
                    var filletEdges is Query = qSubtraction(allEdges, nonEdges);
                    
                    if (definition.filletRad > 0)
                    {
                        try
                        {
                            opFillet(context, id + "fillet1", {
                                "entities" : filletEdges,
                                "radius" : definition.filletRad
                                });
                        }
                    }
                    
                    
                    opShell(context, id + "shell1", {
                            "entities" : qUnion([solid, sideFaces]),
                            "thickness" : -definition.boxWall
                    });
                    /**---------------------------------End of Box Spar Plane Code---------------------------------------**/
                }
            /**----------------------------------------End of shared Spar Plane Code-------------------------------------**/
            }
            if (definition.stiffTab == stiffTab.STRINGER)
            {
            /**--------------------------------------------Start of stringer Code----------------------------------------**/
                var tipPoint = points["LE-Tip"] + definition.tipPos*tipCord*tipNorm - definition.VertTipPos*tipCord*verticalTipDirect/meter;
                
                var basePoint = points["LE-Base"] + definition.basePos*baseCord*baseNorm - definition.VertBasePos*tipCord*verticalDirect/meter;
                
                
                var stringerDist = evDistance(context, {
                                "side0" : basePoint,
                                "side1" : tipPoint
                                }).distance;
                                
                var stringerDirect = basePoint - tipPoint;
                
                var stringerPlanex = stringerDirect/stringerDist;
                
                tipPoint = tipPoint - stringerPlanex*1*meter;
                basePoint = basePoint + stringerPlanex*1*meter;
                
                fCylinder(context, id + "cylinder1", {
                        "topCenter" : tipPoint,
                        "bottomCenter" : basePoint,
                        "radius" : definition.outerDia
                });
                
                solid = qOwnedByBody(qCreatedBy(id +"transform"), EntityType.BODY);
                
                try
                {
                    opBoolean(context, id + "boolean1", {
                        "tools" : qUnion([solid, qCreatedBy(id + "cylinder1", EntityType.BODY)]),
                        "operationType" : BooleanOperationType.INTERSECTION
                        });
                }
                catch (error)
                {
                    throw regenError("Error: the stringer may lie entirely outside the region of the wing", qCreatedBy(id + "cylinder1", EntityType.BODY));
                }
                
                if (definition.stringerType == stringerType.TUBE)
                {
                    if (definition.outerDia <= 2*definition.stringerWall)
                    {
                        throw regenError("Error: Tubular stringer walls are defined to be larger than total diameter", qCreatedBy(id + "boolean1", EntityType.BODY));
                    }
                    
                    fCylinder(context, id + "cylinder2", {
                        "topCenter" : tipPoint,
                        "bottomCenter" : basePoint,
                        "radius" : definition.outerDia -2*definition.stringerWall
                    });
                    
                    try
                    {
                        opBoolean(context, id + "boolean2", {
                                "tools" : qCreatedBy(id + "cylinder2", EntityType.BODY),
                                "targets" : qCreatedBy(id + "boolean1", EntityType.BODY),
                                "operationType" : BooleanOperationType.SUBTRACTION
                        });
                    }
                    catch (error)
                    {
                        throw regenError("Error: An issue occured when attempting to hollow stringer", qUnion([qCreatedBy(id + "boolean1", EntityType.BODY), qCreatedBy(id + "cylinder2", EntityType.BODY)]));
                    }
                }
            /**---------------------------------------------End of stringer Code-----------------------------------------**/ 
            }
        }
    });

const POS_BOUNDS =
{
    (unitless) : [-1, 0, 1]
} as RealBoundSpec;

const WALL_THICK_BOUNDS =
{
    (meter)      : [0.0002, 0.003, 1],
} as LengthBoundSpec;

const OFFSET_BOUNDS =
{
    (meter)      : [0, 0, 1000],
} as LengthBoundSpec;