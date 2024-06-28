Sub CreateMaterial(App As femap.model, matID As Long, title As String, color As Long, matType As Long, Ex As Double, Nuxy As Double, Density As Double)
    ' Create a new material object
    Dim Material As femap.Matl
    Set Material = App.feMatl
    
    ' Set basic properties
    Material.title = title
    Material.color = color
    Material.type = matType
    
    ' Set engineering constants
    Material.Ex = Ex
    Material.Nuxy = Nuxy
    Material.Density = Density
    
    ' Save the material with the specified ID
    Material.Put(matID)
    
    ' Optional: Output a message to confirm creation
    App.feAppMessage(FCM_NORMAL, title & " material created with ID " & matID)
End Sub

Sub Main
    ' Initialize the FEMAP model object
    Dim App As femap.model
    Set App = feFemap()
    
    ' Create Titanium material
    Call CreateMaterial(App, 1, "Titanium", 3, 0, 110000, 0.34, 4.54e-9)
    
    ' Create another material, e.g., Aluminum
    Call CreateMaterial(App, 2, "Aluminum", 4, 0, 69000, 0.33, 2.7e-9)
    
    ' Create a composite material, e.g., Carbon Fiber
    Call CreateMaterial(App, 3, "Carbon Fiber", 5, 1, 230000, 0.2, 1.6e-9)
End Sub
