Sub Main
    ' Initialize the FEMAP model object
    Dim App As femap.model
    Set App = feFemap()
    
    ' Create a new material object
    Dim Material As femap.Matl
    Set Material = App.feMatl
    
    ' Set basic properties
    Material.title = "Titanium"
    Material.color = 3 ' Arbitrary color ID for visual distinction
    Material.type = 0 ' Isotropic material
    
    ' Set engineering constants
    Material.Ex = 110000 ' Young's Modulus in MPa (Example value for Titanium)
    Material.Nuxy = 0.34 ' Poisson's Ratio (Example value for Titanium)
    Material.Density = 4.54e-9 ' Density in tonne/mm^3 (Example value for Titanium)
    
    ' Save the material with ID 1 (or any unique ID)
    Material.Put(1)
    
    ' Optional: Output a message to confirm creation
    App.feAppMessage(FCM_NORMAL, "Titanium material created with ID 1")
End Sub
