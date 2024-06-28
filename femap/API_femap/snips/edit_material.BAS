Sub Main

    Dim App As femap.model
    Set App = feFemap()
    
    ' Create a new material object
    Dim Composite_1 As femap.Matl
    Dim Metal_1 As femap.Matl
    
		Set Composite_1 = App.feMatl
		Set Metal_1 = App.feMatl
    
    ' Set basic properties
    Metal_1.title = "Titanium"
    Metal_1.color = 3 ' Arbitrary color ID for visual distinction
    Metal_1.type = 0 ' Isotropic material
    
    ' Set engineering constants
    Metal_1.Ex = 110000 ' Young's Modulus in MPa (Example value for Titanium)
    Metal_1.Nuxy = 0.34 ' Poisson's Ratio (Example value for Titanium)
    Metal_1.Density = 4.54e-9 ' Density in tonne/mm^3 (Example value for Titanium)
    
    ' Save the material with ID 1 (or any unique ID)
    Metal_1.Put(1)
    
    ' Optional: Output a message to confirm creation
    App.feAppMessage(FCM_NORMAL, "Titanium material created with ID 1")
End Sub
