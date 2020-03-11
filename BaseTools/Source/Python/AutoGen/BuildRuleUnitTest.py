import unittest
from AutoGen.BuildEngine import FileBuildRule
from Common.Misc import PathClass

class TestBuildRule(unittest.TestCase):
    def testBuildOrder(self):
        file_build_rule = FileBuildRule("Asm",["?.asm","?.nasm","?.S","?.s","?.Nasm"],[PathClass("foo.bin")],["nasm"])
        source_list = [PathClass(filename) for filename in ["foo.Nasm","foo.nasm","foo.S"]]
        one_build_order = [".nasm",".Nasm",".S"]
        sec_build_order = [".S",".Nasm",".nasm"]
        for source in source_list:
            dest2 = file_build_rule.Apply(source,sec_build_order)
        self.assertEqual(dest2.Inputs[0].File, "foo.S")

        for source in source_list:
            dest = file_build_rule.Apply(source,one_build_order)
        self.assertEqual(dest.Inputs[0].File, "foo.nasm")

    def testFileBuildRuleInstance(self):
        file_build_rule = FileBuildRule("Asm",["?.asm","?.nasm","?.S","?.s","?.Nasm"],[PathClass("${s_base}.obj")],["nasm"])
        foo_source_list = [PathClass(filename) for filename in ["foo.Nasm"]]
        bar_source_list = [PathClass(filename) for filename in ["bar.S"]]
        
        foo_dest = file_build_rule.Apply(foo_source_list[0])
        
        file_build_rule_1 = file_build_rule.Instantiate()
        bar_dest = file_build_rule_1.Apply(bar_source_list[0])
        
        self.assertNotEqual(id(file_build_rule),id(file_build_rule_1))
        
        self.assertEqual(len(file_build_rule.BuildTargets),len(file_build_rule_1.BuildTargets))
        self.assertEqual(foo_dest.Outputs[0].Path, "foo.obj")
        self.assertEqual(bar_dest.Outputs[0].Path, "bar.obj")

    def testBuildRule(self):
        cmds = [
            'Trim --asm-file -o ${d_path}(+)${s_base}.i -i $(INC_LIST) ${src}',
            '"$(PP)" $(DEPS_FLAGS) $(PP_FLAGS) $(INC) ${src} > ${d_path}(+)${s_base}.ii',
            'Trim --trim-long --source-code -o ${d_path}(+)${s_base}.iii ${d_path}(+)${s_base}.ii',
            '"$(NASM)" -I${s_path}(+) $(NASM_INC) $(NASM_FLAGS) -o $dst ${d_path}(+)${s_base}.iii'
            ]
        file_build_rule = FileBuildRule("Nasm-Assembly-Code-File",["?.nasm"],[PathClass("${s_base}.obj")],cmds)
        foo_source_list = [PathClass(filename) for filename in ["foo.nasm","bar.c"]]
        
        foo_dest = file_build_rule.Apply(foo_source_list[0])
        self.assertEqual(foo_dest.Inputs[0].Path, "foo.nasm")
        self.assertEqual(foo_dest.Outputs[0].Path, "foo.obj")
        self.assertEqual(foo_dest.Commands[0], "Trim --asm-file -o (+)foo.i -i $(INC_LIST) foo.nasm")
        self.assertEqual(foo_dest.Commands[1], '''"$(PP)" $(DEPS_FLAGS) $(PP_FLAGS) $(INC) foo.nasm > (+)foo.ii''')
        self.assertEqual(foo_dest.Commands[2], "Trim --trim-long --source-code -o (+)foo.iii (+)foo.ii")
        self.assertEqual(foo_dest.Commands[3], '''"$(NASM)" -I(+) $(NASM_INC) $(NASM_FLAGS) -o foo.obj (+)foo.iii''')