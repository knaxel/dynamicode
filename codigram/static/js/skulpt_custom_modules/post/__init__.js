// More info on custom modules: https://github.com/bnmnetp/reputablejournal/blob/master/posts/2011/03/adding-a-module-to-skulpt.md

var $builtinmodule = function(name) {

    var mod = {}

    mod.title = new Sk.builtin.str(Sk.postData.title)
    mod.author = new Sk.builtin.str(Sk.postData.author)

    // let blocks = []
    // for (let i=0; i<Sk.postData.blocks.length; i++) {
    //     let block = Sk.postData.blocks[i]
    //     blocks.push({
    //         "name": block.get_name()
    //     })
    // }

    // let f = new Sk.builtin.func(function() {
    //     return new Sk.builtin.str("Hello World")
    // })
    //
    // mod.test = f()

    // mod.blocks = new Sk.builtin.list(blocks)
    
    return mod
}