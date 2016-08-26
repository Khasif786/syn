from syn.type.a import Type as Type_
from syn.type.a import AnyType
from syn.base.b import Attr, init_hook
from .node import Node

#-------------------------------------------------------------------------------
# Query


class Query(Node):
    _opts = dict(min_len = 1,
                 max_len = 1)

    def __call__(self, node, **kwargs):
        if not self._children:
            for x in self.iterate(node):
                yield x
        
        else:
            for c in self.children():
                for n in c(node, **kwargs):
                    for x in self.iterate(n, **kwargs):
                        yield x

    def iterate(self, node, **kwargs):
        if False:
            yield # pragma: no cover


#-------------------------------------------------------------------------------
# Type


class Type(Query):
    _attrs = dict(type = Attr(Type_, AnyType()))
    _opts = dict(args = ('type',))

    @init_hook
    def _dispatch_type(self):
        if not isinstance(self.type, Type_):
            self.type = Type_.dispatch(self.type)

    def iterate(self, node, **kwargs):
        if self.type.query(node):
            yield node


#-------------------------------------------------------------------------------
# Axes


class Axis(Query):
    pass


#-----------------------------------------------------------
# Ancestor


class Ancestor(Axis):
    _attrs = dict(include_self = Attr(bool, False))

    def iterate(self, node, **kwargs):
        for a in node.ancestors(include_self=self.include_self):
            yield a


#-----------------------------------------------------------
# Attribute


class Attribute(Axis):
    def iterate(self, node, **kwargs):
        for attr, value in node.attributes():
            yield attr, value


#-----------------------------------------------------------
# Child


class Child(Axis):
    def iterate(self, node, **kwargs):
        for c in node.children():
            yield c


#-----------------------------------------------------------
# Descendant


class Descendant(Axis):
    _attrs = dict(include_self = Attr(bool, False))

    def iterate(self, node, **kwargs):
        for d in node.descendants(include_self=self.include_self):
            yield d


#-----------------------------------------------------------
# Parent


class Parent(Axis):
    def iterate(self, node, **kwargs):
        yield node.parent()


#-----------------------------------------------------------
# Root


class Root(Axis):
    def iterate(self, node, **kwargs):
        yield node.root()


#-----------------------------------------------------------
# Self


class Self(Axis):
    def iterate(self, node, **kwargs):
        yield node


#-----------------------------------------------------------
# Sibling


class Sibling(Axis):
    _attrs = dict(following = Attr(bool, False),
                  preceding = Attr(bool, False))
    _opts = dict(one_true = [('following', 'preceding')])

    def iterate(self, node, **kwargs):
        for d in node.siblings(following=self.following, 
                               preceding=self.preceding, 
                               axis=True):
            yield d


#-------------------------------------------------------------------------------
