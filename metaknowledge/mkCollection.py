import copy
import os.path
import collections.abc

from .mkExceptions import CollectionTypeError

class Collection(collections.abc.MutableSet, collections.abc.Hashable):
    def __init__(self, inSet, allowedTypes, collectedTypes, name, bad, errors, quietStart = False):
        """Mostly based on RecordCollection 1.0 with some improvents/tweaks"""
        self._collection = inSet
        self._allowedTypes = allowedTypes
        self._collectedTypes = collectedTypes

        self.name = name
        self.bad = bad
        self.errors = errors

    #Hashable method

    def __hash__(self):
        return hash(sum((hash(i) for i in self)))

    #Set methods

    def __le__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            return len(self) <= len(other)

    def __ge__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            return len(self) >= len(other)

    def __eq__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            return self._collection == other._collection

    def __len__(self):
        return len(self._collection)

    def __iter__(self):
        for i in self._collection:
            yield i

    def __contains__(self, item):
        return item in self._collection

    #Mutable Set methods

    def add(self, elem):
        if isinstance(elem, self._allowedTypes):
            self._collection.add(elem)
            self._collectedTypes.add(type(elem).__name__)
        else:
            raise CollectionTypeError("{} can only contain '{}', '{}' is not allowed.".format(type(self).__name__, self._allowedTypes, elem))

    def discard(self, elem):
        return self._Grants.discard(elem)

    def remove(self, elem):
        try:
            return self._collection.remove(elem)
        except KeyError:
            raise KeyError("'{}' was not found in the {}: '{}'.".format(elem, type(self).__name__, self)) from None

    def clear(self):
        self.bad = False
        self.errors = {}
        self._collection.clear()

    def pop(self):
        try:
            return self._collection.pop()
        except KeyError:
            raise KeyError("Nothing left in the {}: '{}'.".format(type(self).__name__, self)) from None

    def __ior__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            self._collection |= other._collection
            self._collectedTypes |= other._collectedTypes
            self.name = name = '{} |= {}'.format(self.name, other.name)
            if other.bad or self.bad:
                self.bad = True
                self.errors.update(other.errors)
            return self

    def __iand__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            self._collection &= other._collection
            self._collectedTypes |= other._collectedTypes
            self.name = name = '{} &= {}'.format(self.name, other.name)
            if other.bad or self.bad:
                self.bad = True
                self.errors.update(other.errors)
            return self

    def __ixor__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            self._collection ^= other._collection
            self._collectedTypes |= other._collectedTypes
            self.name = name = '{} ^= {}'.format(self.name, other.name)
            if other.bad or self.bad:
                self.bad = True
                self.errors.update(other.errors)
            return self

    def __isub__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            self._collection -= other._collection
            self._collectedTypes |= other._collectedTypes
            self.name = name = '{} -= {}'.format(self.name, other.name)
            if other.bad or self.bad:
                self.bad = True
                self.errors.update(other.errors)
            return self

    #These are provided by the above
    #but don't work right unless they are custom written

    def __or__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            retCollection = type(self)(self._collection | other._collection, name = '{} | {}'.format(self.name, other.name), quietStart = True)
            if other.bad or self.bad:
                retCollection.bad = True
                retCollection.errors.update(other.errors)
            return retCollection

    def __and__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            retCollection = type(self)(self._collection & other._collection, name = '{} & {}'.format(self.name, other.name), quietStart = True)
            if other.bad or self.bad:
                retCollection.bad = True
                retCollection.errors.update(other.errors)
            return retCollection

    def __sub__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            retCollection = type(self)(self._collection - other._collection, name = '{} - {}'.format(self.name, other.name), quietStart = True)
            if other.bad or self.bad:
                retCollection.bad = True
                retCollection.errors.update(other.errors)
            return retCollection

    def __xor__(self, other):
        if type(self) != type(other):
            return NotImplemented
        else:
            retCollection = type(self)(self._collection ^ other._collection, name = '{} ^ {}'.format(self.name, other.name), quietStart = True)
            if other.bad or self.bad:
                retCollection.bad = True
                retCollection.errors.update(other.errors)
            return retCollection

    def __repr__(self):
        return "<metaknowledge.{} object {}>".format(type(self).__name__, self.name)

    def __str__(self):
        return "{}({})".format(type(self).__name__, self.name)

    def copy(self):
        collectedCopy = copy.copy(self)
        collectedCopy._collection = collectedCopy._collection.copy()
        self._collectedTypes = self._collectedTypes.copy()
        self._allowedTypes = self._allowedTypes.copy()
        collectedCopy.errors = collectedCopy.errors.copy()
        return collectedCopy

    def peak(self):
        if len(self._collection) > 0:
            return self._collection.__iter__().__next__()
        else:
            return None
