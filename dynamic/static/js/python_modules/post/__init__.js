// More info on custom modules: https://github.com/bnmnetp/reputablejournal/blob/master/posts/2011/03/adding-a-module-to-skulpt.md

var $builtinmodule = function(name) {

    var mod = {}
    var set_header = function(text) {
        document.getElementById("title").innerHTML = text.toString()
    }
    
    
    mod.set_header = new Sk.builtin.func(function(a) {
        return set_header(a)
    })
    
    return mod
}