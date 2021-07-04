
// let codeEditor = createSkulptInterface("codeEditor")
// let outputEditor = createSkulptInterface("outputEditor", isCodeInput=false)
// codeEditor.setSize(null, 200)
// outputEditor.setSize(null, 200)

// $("#inputBar").hide()
// setInterfaceElements(codeEditor, outputEditor, "inputBar")

let code_runner = new CodeRunner("codeEditor", "outputEditor", "inputBar",
    "runButton", "stopButton")
code_runner.setEditorSize(null, 200)