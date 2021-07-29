// More info on custom modules: https://github.com/bnmnetp/reputablejournal/blob/master/posts/2011/03/adding-a-module-to-skulpt.md

/*

To write a function:
mod.FUNC_NAME = new Sk.builtin.func(function(... args ...) {...})

To call a function or instantiate a class within the module:
mod.FUNC_NAME.tp$call([ ... args ... ])

To create a class:
mod.CLASS_NAME = Sk.misceval.buildClass(mod, function($glb, $loc) {
        $loc.__init__ = new Sk.builtin.func(function(self, ...args...) {
            ...
        })


    }, "CLASS_NAME", [])

To create a variable in a class:
self.$d.entries.VAR_NAME = [
    new Sk.builtin.str("VAR_NAME"),
    VAR_VALUE
]

 */


let $builtinmodule = function (name) {

    let mod = {};

    mod.title = new Sk.builtin.str(Sk.codepageData.title)
    mod.author = new Sk.builtin.str(Sk.codepageData.author)

    mod.blocks = Sk.codepageData.blocks
    mod.get_block = new Sk.builtin.func(function(block_name) {
        return Sk.codepageData.get_block(block_name)
    })

    return mod
};