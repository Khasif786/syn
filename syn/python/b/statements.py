import ast
from .base import PythonNode, Attr, AST, ACO, col_offset
from syn.base_utils import setitem, get_typename
from syn.type.a import List
from syn.five import STR

#-------------------------------------------------------------------------------
# Statement


class Statement(PythonNode):
    _opts = dict(max_len = 0)


#-------------------------------------------------------------------------------
# Assign


class Assign(Statement):
    _attrs = dict(targets = Attr(List(PythonNode), groups=(AST, ACO)),
                  value = Attr(PythonNode, groups=(AST, ACO)))
    _opts = dict(args = ('targets', 'value'))

    def emit(self, **kwargs):
        with setitem(kwargs, 'col_offset', 0):
            targs = [targ.emit(**kwargs) for targ in self.targets]
            val = self.value.emit(**kwargs)

        ret = ' ' * col_offset(self, kwargs)
        ret += ' = '.join(targs)
        ret += ' = ' + val
        return ret


#-------------------------------------------------------------------------------
# Return


class Return(Statement):
    _attrs = dict(value = Attr(PythonNode, groups=(AST, ACO)))

    def emit(self, **kwargs):
        with setitem(kwargs, 'col_offset', 0):
            val = self.value.emit(**kwargs)

        ret = ' ' * col_offset(self, kwargs)
        ret += 'return ' + val
        return ret


#-------------------------------------------------------------------------------
# Import


class Alias(Statement):
    ast = ast.alias
    _attrs = dict(name = Attr(STR, group=AST),
                  asname = Attr(STR, optional=True, group=AST))
    _opts = dict(args = ('name', 'asname'))

    def emit(self, **kwargs):
        ret = self.name
        if self.asname:
            ret += ' as ' + self.asname
        return ret


class Import(Statement):
    _attrs = dict(names = Attr(List(Alias), groups=(AST, ACO)))

    def emit(self, **kwargs):
        with setitem(kwargs, 'col_offset', 0):
            strs = [val.emit(**kwargs) for val in self.names]
            names = ', '.join(strs)

        ret = ' ' * col_offset(self, kwargs)
        ret += 'import ' + names
        return ret


#-------------------------------------------------------------------------------
# Empty Statements


class EmptyStatement(Statement):
    def emit(self, **kwargs):
        ret = ' ' * col_offset(self, kwargs)
        ret += get_typename(self).lower()
        return ret


class Break(EmptyStatement):
    pass


class Continue(EmptyStatement):
    pass


class Pass(EmptyStatement):
    pass


#-------------------------------------------------------------------------------
# __all__

__all__ = ('Statement',
           'Assign', 'Return',
           'Alias', 'Import',
           'EmptyStatement', 'Break', 'Continue', 'Pass')

#-------------------------------------------------------------------------------
