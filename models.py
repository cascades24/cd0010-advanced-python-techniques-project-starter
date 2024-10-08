"""Represent models for near-Earth objects and their close approaches.

The `NearEarthObject` class represents a near-Earth object. Each has a unique
primary designation, an optional unique name, an optional diameter, and a flag
for whether the object is potentially hazardous.

The `CloseApproach` class represents a close approach to Earth by an NEO. Each
has an approach datetime, a nominal approach distance, and a relative approach
velocity.

A `NearEarthObject` maintains a collection of its close approaches, and a
`CloseApproach` maintains a reference to its NEO.

"""
from helpers import cd_to_datetime, datetime_to_str


class NearEarthObject:
    """A near-Earth object (NEO).

    An NEO encapsulates semantic and physical parameters about the object, such
    as its primary designation (required, unique), IAU name (optional), diameter
    in kilometers (optional - sometimes unknown), and whether it's marked as
    potentially hazardous to Earth.

    A `NearEarthObject` also maintains a collection of its close approaches -
    initialized to an empty collection, but eventually populated in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `NearEarthObject`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """

        #setting designation
        self.designation = str(info.get('designation',''))

        #setting name
        if info.get('name','') == '':
            self.name = None
        else:
            self.name = str(info['name'])
        
        #setting diameter
        if info.get('diameter') == '':
            self.diameter = float('nan')
        else:
            self.diameter = float(info.get('diameter'))

        #setting hazardous values
        if info.get('hazardous',None) == None:
            self.hazardous = False
        else:
            if str(info['hazardous']) == 'Y':
                self.hazardous = True
            else:
                self.hazardous = False

        # Create an empty initial collection of linked approaches.
        self.approaches = list()


    @property
    def fullname(self):
        """Return a representation of the full name of this NEO."""
        return f"{self.designation} ({self.name})"
    

    def __str__(self):
        """Return `str(self)`."""
        
        #defining the modified for the string for the hazardous parameter
        if self.hazardous:
            mod_string = "is"
        else:
            mod_string = "is not"

        return f"A NearEarthObject with the designation {self.designation} and the name {self.name}," \
               f" with a diameter of {self.diameter:.1f}km, and {mod_string} potentially hazardous"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"NearEarthObject(designation={self.designation!r}, name={self.name!r}, " \
               f"diameter={self.diameter:.3f}, hazardous={self.hazardous!r})"

    def serialize(self):
        """Return a dictionary of the object attributes in a way
        that prepares it for printing to a file (CSV or JSON)

        :return serial_dict: a dictionary with formatted attributes about the object
        """
        self.serial_dict = dict()

        #name
        if self.name == None:
            self.serial_dict['name'] = ''
        else:
            self.serial_dict['name'] = self.name

        #designation
        self.serial_dict['designation'] = self.designation

        #assigning diameter
        #testing for NaN by seeing if it equals itself
        #if self.diameter != self.diameter:
        #    self.serial_dict['diameter'] = float('nan')
        #else:
        #    self.serial_dict = self.diameter
        self.serial_dict['diameter_km'] = self.diameter

        #adding the hazardous parameter to the dictionary 
        self.serial_dict['potentially_hazardous']= self.hazardous

        #adding the list of close approaches
        #self.serial_dict['approaches'] = self.approaches

        return self.serial_dict



class CloseApproach:
    """A close approach to Earth by an NEO.

    A `CloseApproach` encapsulates information about the NEO's close approach to
    Earth, such as the date and time (in UTC) of closest approach, the nominal
    approach distance in astronomical units, and the relative approach velocity
    in kilometers per second.

    A `CloseApproach` also maintains a reference to its `NearEarthObject` -
    initially, this information (the NEO's primary designation) is saved in a
    private attribute, but the referenced NEO is eventually replaced in the
    `NEODatabase` constructor.
    """

    def __init__(self, **info):
        """Create a new `CloseApproach`.

        :param info: A dictionary of excess keyword arguments supplied to the constructor.
        """
        #assigning designation
        self._designation= str(info.get('designation',''))
        #assigning time
        if info.get('time',None) != None:
            self.time = cd_to_datetime(info.get('time'))  #Done: Use the cd_to_datetime function for this attribute.
        else:
            self.time = None
        #assigning distance
        self.distance = float(info.get('distance',0))
        #assigning velocity
        self.velocity = float(info.get('velocity',0))

        # Create an attribute for the referenced NEO, originally None.
        self.neo = None

    @property
    def time_str(self):
        """Return a formatted representation of this `CloseApproach`'s approach time.
        """
        return f"{datetime_to_str(self.time)}"
   
    @property
    def fullname(self):
        """Return a representation of the full name of this close approach."""
        # Done: Use self.designation and self.name to build a fullname for this object.
        return f"{self.neo} ({datetime_to_str(self.time)})"

    def __str__(self):
        """Return `str(self)`."""
        
        #for some reason need to force the variables to floats again 
        return f"At {datetime_to_str(self.time)}, {self.neo.fullname} passes by Earth at {float(self.distance):.4f}AU, " \
               f" with relative velocity of {float(self.velocity):.2f} km/s"

    def __repr__(self):
        """Return `repr(self)`, a computer-readable string representation of this object."""
        return f"CloseApproach(time={self.time_str!r}, distance={float(self.distance):.2f}, " \
               f"velocity={float(self.velocity):.4f}, neo={self.neo!r})"
    

    def serialize(self):
        """Return a dictionary of the object attributes in a way
        that prepares it for printing to a file (CSV or JSON)

        :return serial_dict: a dictionary with formatted attributes about the object
        """

        #defining the empty dictionary
        self.serial_dict = dict()
    
        #putting date into string from datetime
        self.serial_dict['datetime_utc'] = datetime_to_str(self.time)

        #distance param
        self.serial_dict['distance_au'] = self.distance

        #velocity param
        self.serial_dict['velocity_km_s'] = self.velocity

        #neo param
        self.serial_dict['neo'] = self.neo.serialize()

        return self.serial_dict



    