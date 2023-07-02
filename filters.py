"""Provide filters for querying close approaches and limit the generated results.

The `create_filters` function produces a collection of objects that is used by
the `query` method to generate a stream of `CloseApproach` objects that match
all of the desired criteria. The arguments to `create_filters` are provided by
the main module and originate from the user's command-line options.

This function can be thought to return a collection of instances of subclasses
of `AttributeFilter` - a 1-argument callable (on a `CloseApproach`) constructed
from a comparator (from the `operator` module), a reference value, and a class
method `get` that subclasses can override to fetch an attribute of interest from
the supplied `CloseApproach`.

The `limit` function simply limits the maximum number of values produced by an
iterator.

"""
import datetime
import itertools

class Filters:
    """Class to contain all of the filters for easy calling in the query function
    
    :param distance_filter: the AttributeType class object with the distance filter data
    :param diameter_filter: the AttributeType class object with the diameter filter data
    :param velocity_filter: the AttributeType class object with the distance filter data
    :param date_filter: the DateAttr class object with the date filter data
    :param hazard_filter: the HazzardAttr class object with the hazard filter data
    
    """
    def __init__(self,distance_filter,diameter_filter,
                 velocity_filter,date_filter,hazard_filter):
        self.distance_filter = distance_filter
        self.diameter_filter = diameter_filter
        self.velocity_filter = velocity_filter
        self.date_filter = date_filter
        self.hazard_filter = hazard_filter

class AttributeType:
    """General Class for numerical value filters like distance, """
    def __init__(self,attribute_name,attribute_max,attribute_min):
        """Construct a new Attribute Type filter for numerical filters given attribute name, min, and max

        This class serves as collection for the paramters categorized by type, i.e. diameter

        :param attribute_name: attribute name (i.e. diameter).
        :param attribute_max: Maximum attribute value as passed into constructor
        :param attribute_min: Minimum attribute value as passed into constructor
        """
        self.attribute_name = attribute_name
        if attribute_max != None and type(attribute_max) != datetime.date:
            self.attribute_max = float(attribute_max)
        else:
            self.attribute_max = attribute_max

        if attribute_min != None and type(attribute_min) != datetime.date:
            self.attribute_min = float(attribute_min)
        else:
            self.attribute_min = attribute_min

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"{self.__class__.__name__}(attribute_name={self.attribute_name},"\
            f" attribute_max={self.attribute_max}, "\
            f" attribute_min={self.attribute_min})"

class DateAttr(AttributeType):
    def __init__(self,attribute_name, attribute_max, attribute_min,on_date):
        super().__init__(attribute_name, attribute_max, attribute_min)
        """Construct a subclass of Attribute Type for the date filter

        This class serves as collection for the paramters categorized by type, 
        and including a parameter for a singular date

        :param attribute_name: attribute name (i.e. diameter).
        :param attribute_max: Maximum attribute value as passed into constructor
        :param attribute_min: Minimum attribute value as passed into constructor
        :param on_date: A singular data provided into the filter 
        """
        #approaches on the current date 
        if on_date != None:
            if type(on_date) is not datetime.date:
                self.on_date = datetime.datetime.strptime(on_date,"%Y-%m-%d")
            else:
                self.on_date = on_date
        else: 
            self.on_date = None
    
    
class HazardAttr:
    def __init__(self,attribute_name,hazardous):

        self.attribute_name = attribute_name
        #this gets passed in as a bool by the args function
        self.hazardous = hazardous

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"{self.__class__.__name__}(attribute_name={self.attribute_name},"\
            f" hazardous={self.hazardous}, "

def create_filters(
        date=None, start_date=None, end_date=None,
        distance_min=None, distance_max=None,
        velocity_min=None, velocity_max=None,
        diameter_min=None, diameter_max=None,
        hazardous=None
):
    """Create a collection of filters from user-specified criteria.

    Each of these arguments is provided by the main module with a value from the
    user's options at the command line. Each one corresponds to a different type
    of filter. For example, the `--date` option corresponds to the `date`
    argument, and represents a filter that selects close approaches that occurred
    on exactly that given date. Similarly, the `--min-distance` option
    corresponds to the `distance_min` argument, and represents a filter that
    selects close approaches whose nominal approach distance is at least that
    far away from Earth. Each option is `None` if not specified at the command
    line (in particular, this means that the `--not-hazardous` flag results in
    `hazardous=False`, not to be confused with `hazardous=None`).

    The return value must be compatible with the `query` method of `NEODatabase`
    because the main module directly passes this result to that method. For now,
    this can be thought of as a collection of `AttributeFilter`s.

    :param date: A `date` on which a matching `CloseApproach` occurs.
    :param start_date: A `date` on or after which a matching `CloseApproach` occurs.
    :param end_date: A `date` on or before which a matching `CloseApproach` occurs.
    :param distance_min: A minimum nominal approach distance for a matching `CloseApproach`.
    :param distance_max: A maximum nominal approach distance for a matching `CloseApproach`.
    :param velocity_min: A minimum relative approach velocity for a matching `CloseApproach`.
    :param velocity_max: A maximum relative approach velocity for a matching `CloseApproach`.
    :param diameter_min: A minimum diameter of the NEO of a matching `CloseApproach`.
    :param diameter_max: A maximum diameter of the NEO of a matching `CloseApproach`.
    :param hazardous: Whether the NEO of a matching `CloseApproach` is potentially hazardous.
    :return: A class object of Filters with stored for use with `query`.
    """
    
    #builing the class object with the filters 
    filters = Filters(AttributeType("Distance",distance_max,distance_min),
                      AttributeType("Diameter",diameter_max,diameter_min),
                      AttributeType("Velocity",velocity_max,velocity_min),
                      DateAttr("Date",end_date,start_date,date),
                      HazardAttr("Hazardous",hazardous))

    return filters


def limit(iterator, n=None):
    """Produce a limited stream of values from an iterator.

    If `n` is 0 or None, don't limit the iterator at all.

    :param iterator: An iterator of values.
    :param n: The maximum number of values to produce.
    :yield: The first (at most) `n` values from the iterator.
    """
    #if condition if n is not None and not zero 
    if n != None and n != 0:
        return itertools.islice(iterator, n)
    else:
        return iterator
