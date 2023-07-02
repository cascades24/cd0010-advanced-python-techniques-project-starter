"""A database encapsulating collections of near-Earth objects and their close approaches.

A `NEODatabase` holds an interconnected data set of NEOs and close approaches.
It provides methods to fetch an NEO by primary designation or by name, as well
as a method to query the set of close approaches that match a collection of
user-specified criteria.

"""


class NEODatabase:
    """A database of near-Earth objects and their close approaches.

    A `NEODatabase` contains a collection of NEOs and a collection of close
    approaches. It additionally maintains a few auxiliary data structures to
    help fetch NEOs by primary designation or by name and to help speed up
    querying for close approaches that match criteria.
    """
    def __init__(self, neos, approaches):
        """Create a new `NEODatabase`.

        As a precondition, this constructor assumes that the collections of NEOs
        and close approaches haven't yet been linked - that is, the
        `.approaches` attribute of each `NearEarthObject` resolves to an empty
        collection, and the `.neo` attribute of each `CloseApproach` is None.

        However, each `CloseApproach` has an attribute (`._designation`) that
        matches the `.designation` attribute of the corresponding NEO. This
        constructor modifies the supplied NEOs and close approaches to link them
        together - after it's done, the `.approaches` attribute of each NEO has
        a collection of that NEO's close approaches, and the `.neo` attribute of
        each close approach references the appropriate NEO.

        :param neos: A collection of `NearEarthObject`s.
        :param approaches: A collection of `CloseApproach`es.
        """
        self._neos = neos
        self._approaches = approaches

        #making dictionaries of NEOs by des and name for easier searching
        #neo name dict
        self._neo_name_dict = {neo.name:neo for neo in self._neos if neo.name != None}
        #neo designation dict
        self._neo_des_dict = {neo.designation:neo for neo in self._neos}

        #linking together NEOs and approaches
        for approach in self._approaches:
            approach.neo = self._neo_des_dict[approach._designation]
            #print(approach.neo.diameter)
            self._neo_des_dict[approach._designation].approaches.append(approach)



    def get_neo_by_designation(self, designation):
        """Find and return an NEO by its primary designation.

        If no match is found, return `None` instead.

        Each NEO in the data set has a unique primary designation, as a string.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param designation: The primary designation of the NEO to search for.
        :return: The `NearEarthObject` with the desired primary designation, or `None`.
        """
        #searching through dictionary:
        neo = self._neo_des_dict.get(designation,None)

        return neo

    def get_neo_by_name(self, name):
        """Find and return an NEO by its name.

        If no match is found, return `None` instead.

        Not every NEO in the data set has a name. No NEOs are associated with
        the empty string nor with the `None` singleton.

        The matching is exact - check for spelling and capitalization if no
        match is found.

        :param name: The name, as a string, of the NEO to search for.
        :return: The `NearEarthObject` with the desired name, or `None`.
        """
        #searching through dictionary:
        neo = self._neo_name_dict.get(name,None)

        return neo

    def query(self, filters=()):
        """Query close approaches to generate those that match a collection of filters.

        This generates a stream of `CloseApproach` objects that match all of the
        provided filters.

        If no arguments are provided, generate all known close approaches.

        The `CloseApproach` objects are generated in internal order, which isn't
        guaranteed to be sorted meaningfully, although is often sorted by time.

        :param filters: A collection of filters capturing user-specified criteria.
        :return: A stream of matching `CloseApproach` objects.
        """
    
        for approach in self._approaches:
            
            #setting singular truth variable that will get set to False if there any of the statements don't pass
            approach_valid = True


            #put in if statements to break it out from one since if statement
            #multiple lines is longer but is more readable 
            
            ###########################
            #distance compares
            #min distance
            if (filters.distance_filter.attribute_min != None
                and approach.distance < filters.distance_filter.attribute_min):
                #setting to false if the approach distance min is < the minumum distance
                approach_valid = False

            #max distance
            if (filters.distance_filter.attribute_max != None 
                and approach.distance > filters.distance_filter.attribute_max):
                #setting to false if the approach distance max is > the maximum distance
                approach_valid = False

            ############################
            #diameter compares
            #min diameter
            #testing for none filter types, diameter size, and isNan
            if (filters.diameter_filter.attribute_min != None 
                and (approach.neo.diameter < filters.diameter_filter.attribute_min 
                     or approach.neo.diameter != approach.neo.diameter)):
                #setting to false if the diameter min is < the minumum diameter
                approach_valid = False
            #else:
                #if approach.neo.diameter != float('nan'):
                #    print(approach.neo.name)
                #    print(approach.neo.diameter)
                #    print(filters.diameter_filter.attribute_min)

            #max diameter
            if (filters.diameter_filter.attribute_max != None 
                and (approach.neo.diameter > filters.diameter_filter.attribute_max 
                     or approach.neo.diameter != approach.neo.diameter)):
                #setting to false if the approach diameter max is > the maximum diameter
                approach_valid = False

            ############################
            #velocity compare
            #min velocity
            if (filters.velocity_filter.attribute_min != None 
                and approach.velocity < filters.velocity_filter.attribute_min):
                #setting to false if the velocity min is < the minumum velocity
                approach_valid = False

            #max velocity
            if (filters.velocity_filter.attribute_max != None 
                and approach.velocity > filters.velocity_filter.attribute_max):
                #setting to false if the approach velocity max is > the maximum velocity
                approach_valid = False

            #############################
            #hazardous compare
            if (filters.hazard_filter.hazardous != None 
                and approach.neo.hazardous != filters.hazard_filter.hazardous):
                #seeing if bool matches with the bool from the approach
                approach_valid = False

            ##########################
            #time compare
            if (filters.date_filter.on_date != None 
                and approach.time.date() != filters.date_filter.on_date):
                #seeing if date matches as expected
                #print(filters.date_filter.on_date)
                #print(approach.time)
                #print("comparing dates: " + str(approach.time == filters.date_filter.on_date))
                approach_valid = False
            elif approach.time == filters.date_filter.on_date:
                print(filters.date_filter.on_date)
                print(type(approach.time.date()))
                print(type(filters.date_filter.on_date))
                print(approach.time)
            
            #min date
            if (filters.date_filter.attribute_min != None 
                and approach.time.date() < filters.date_filter.attribute_min):
                #setting to false if the date min is < the minumum date
                approach_valid = False

            #max date
            if (filters.date_filter.attribute_max != None 
                and approach.time.date() > filters.date_filter.attribute_max):
                #setting to false if the approach date max is > the maximum date
                approach_valid = False

            
            #if all statements pass 
            if approach_valid:
                yield approach

        
