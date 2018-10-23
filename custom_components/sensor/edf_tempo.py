"""
Support for ejp site.


configuration.yaml

sensor:
  - platform: edf_tempo

"""
import logging
from datetime import timedelta
from datetime import datetime
import requests
import voluptuous as vol

from homeassistant.components.sensor import PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from homeassistant.const import ( CONF_RESOURCES)
from homeassistant.util import Throttle
from homeassistant.helpers.entity import Entity

__version__ = '0.0.1'

_LOGGER = logging.getLogger(__name__)

MIN_TIME_BETWEEN_UPDATES = timedelta(days=1)
now = datetime.today()

SENSOR_PREFIX = 'Tempo '

SENSOR_TYPES = {
    'jourj': ['Today', '', 'mdi:flash'],
    'jourj1': ['Tomorrow', '', 'mdi:flash'],
    'white-remainingdays': ['nomdre de jour blanc restant', '', 'mdi:counter'],
    'blue-remainingdays': ['nomdre de jour bleu restant', '', 'mdi:counter'],
    'red-remainingdays': ['nomdre de jour rouge restant', '', 'mdi:counter'],
    'white-totaldays': ['nomdre de jour blanc total', '', 'mdi:counter'],
    'blue-totaldays': ['nomdre de jour bleu total', '', 'mdi:counter'],
    'red-totaldays': ['nomdre de jour rouge total', '', 'mdi:counter']
}

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend({})


def setup_platform(hass, config, add_entities, discovery_info=None):
    """Setup the tempo sensors."""

    try:
        data = TempoData()
    except requests.exceptions.HTTPError as error:
        _LOGGER.error(error)
        return False

    entities = []

    for resource in SENSOR_TYPES:
        sensor_type = resource.lower()
        entities.append(TempoSensor(data, sensor_type))

    add_entities(entities)


# pylint: disable=abstract-method
class TempoData(object):
    """Representation of a Tempo data."""

    def __init__(self):
        """Initialize the data."""
        self.data = None
        self.dataRemaining = None
        self.paramBlue = None
        self.paramWhite = None
        self.paramRed = None
        
    @Throttle(MIN_TIME_BETWEEN_UPDATES)
    def update(self):
        """Update the data."""
        try:
            """"""
            self.data = requests.get('https://particulier.edf.fr/bin/edf_rc/servlets/ejptemponew?Date_a_remonter='+now.strftime('%Y-%m-%d')+'&TypeAlerte=TEMPO', timeout=5).json()
            self.dataRemaining = requests.get('https://particulier.edf.fr/bin/edf_rc/servlets/ejptempodaysnew?TypeAlerte=TEMPO', timeout=5).json()
            self.paramBlue = requests.get('https://particulier.edf.fr/services/rest/referentiel/getConfigProperty?PARAM_CONFIG_PROPERTY=param.nb.bleu.periode', timeout=5).json()["param.nb.bleu.periode"]
            self.paramWhite = requests.get('https://particulier.edf.fr/services/rest/referentiel/getConfigProperty?PARAM_CONFIG_PROPERTY=param.nb.blanc.periode', timeout=5).json()["param.nb.blanc.periode"]
            self.paramRed = requests.get('https://particulier.edf.fr/services/rest/referentiel/getConfigProperty?PARAM_CONFIG_PROPERTY=param.nb.rouge.periode', timeout=5).json()["param.nb.rouge.periode"]
            _LOGGER.debug("Data = %s", self.data)
        except requests.exceptions.RequestException:
            _LOGGER.error("Error occurred while fetching data.")
            self.data = None
            self.dataRemaining = None
            self.paramBlue = None
            self.paramWhite = None
            self.paramRed = None
            return False

class TempoSensor(Entity):
    """Representation of a Tempo Sensor."""

    def __init__(self, data, sensor_type):
        """Initialize the sensor."""
        self.data = data
        self.type = sensor_type
        self._name = SENSOR_PREFIX + SENSOR_TYPES[self.type][0]
        self._unit = SENSOR_TYPES[self.type][1]
        self._icon = SENSOR_TYPES[self.type][2]
        self._state = None

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return self._icon

    @property
    def state(self):
        """Return the state of the sensor. (total/current power consumption/production or total gas used)"""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit

    def update(self):
        """Get the latest data and use it to update our sensor state."""
        self.data.update()
        energy = self.data.data
        energyRemaining = self.data.dataRemaining

        if self.type == 'jourj':
            self._state = energy["JourJ"]["Tempo"]
        elif self.type == 'jourj1':
            self._state = energy["JourJ1"]["Tempo"]
        elif self.type == 'white-remainingdays':
            self._state = energyRemaining["PARAM_NB_J_BLANC"]
        elif self.type == 'red-remainingdays':
            self._state = energyRemaining["PARAM_NB_J_ROUGE"]
        elif self.type == 'blue-remainingdays':
            self._state = energyRemaining["PARAM_NB_J_BLEU"]
        elif self.type == 'white-totaldays':
            self._state = self.data.paramWhite
        elif self.type == 'red-totaldays':
            self._state = self.data.paramRed
        elif self.type == 'blue-totaldays':
            self._state = self.data.paramBlue         

