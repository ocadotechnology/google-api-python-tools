import datetime

from dateutil.relativedelta import relativedelta


class Constant(object):
    @classmethod
    def describe(cls, obj):
        raise NotImplementedError

    @classmethod
    def get_all(cls):
        raise NotImplementedError

    @classmethod
    def describe_all(cls):
        descriptions = "\n\n".join([cls.describe(obj) for obj in cls.get_all()])
        return "Available options are:\n%s" % descriptions


class ComputeEngineZones(Constant):
    description = {
        'europe-west1-b': {
            '32-core': False
        },
        'europe-west1-c': {
            '32-core': True
        },
        'europe-west1-d': {
            '32-core': True
        },
    }

    @classmethod
    def describe(cls, zone):
        return "Zone %s: 32-core machines are%s available" % (
            zone, "" if cls.description[zone]['32-core'] else " not"
        )

    @classmethod
    def get_all(cls):
        return sorted(cls.description.keys())


class ComputeEngineMachineType(Constant):
    DATAPROC_FEE_PER_CORE = 0.01
    basic_types = {
        'standard': {
            'cpu': 1,
            'memory': 3.75,
            'price': 0.05
        },
        'highmem': {
            'cpu': 1,
            'memory': 6.5,
            'price': 0.063
        },
        'highcpu': {
            'cpu': 1,
            'memory': 0.9,
            'price': 0.038
        }
    }

    @classmethod
    def get_number_of_cores_for(cls, machine_type):
        return cls._calculate_value_for(machine_type, 'cpu')

    @classmethod
    def get_amount_of_memory_in_gb(cls, machine_type):
        return cls._calculate_value_for(machine_type, 'memory')

    @classmethod
    def get_per_hour_price_for(cls, machine_type):
        return cls._calculate_value_for(machine_type, 'price') + cls.get_number_of_cores_for(
            machine_type) * cls.DATAPROC_FEE_PER_CORE

    @classmethod
    def _calculate_value_for(cls, machine_type, dimension):
        _, basic_type, multiplier = machine_type.split('-')
        return cls.basic_types[basic_type][dimension] * int(multiplier)

    @classmethod
    def describe(cls, machine_type):
        return ("Machine %s\n"
                "Number of VCPU: %s\n"
                "Amount of memory (GB): %s\n"
                "Price per hour: %s$") % (
                   machine_type,
                   cls.get_number_of_cores_for(machine_type),
                   cls.get_amount_of_memory_in_gb(machine_type),
                   cls.get_per_hour_price_for(machine_type)
               )

    @classmethod
    def get_all(cls):
        all_types = []
        for basic_type in cls.basic_types.keys():
            all_types += ['n1-%s-%s' % (basic_type, 2 ** i) for i in range(1, 6)]
        return all_types


class DataprocImageVersion(Constant):
    V_0_1 = "0.1"
    V_0_2 = "0.2"
    V_1_0 = "1.0"

    description = {
        V_1_0: {
            "release": datetime.date(2015, 11, 18),
            "components": {
                "Spark": "1.6.0",
                "Hadoop": "2.7.2",
                "Pig": "0.15.0",
                "Hive": "1.2.1",
                "GCS connector": "1.4.4-hadoop2",
                "BigQuery connector": "0.7.4-hadoop2"
            }
        },
        V_0_2: {
            "release": datetime.date(2015, 11, 18),
            "components": {
                "Spark": "1.5.2",
                "Hadoop": "2.7.1",
                "Pig": "0.15.0",
                "Hive": "1.2.1",
                "GCS connector": "1.4.3-hadoop2",
                "BigQuery connector": "0.7.3-hadoop2"
            }
        },
        V_0_1: {
            "release": datetime.date(2015, 9, 23),
            "components": {
                "Spark": "1.5.0",
                "Hadoop": "2.7.1",
                "Pig": "0.14.10",
                "Hive": "1.0",
                "GCS connector": "1.4.2-hadoop2",
                "BigQuery connector": "0.7.2-hadoop2"
            }
        }
    }

    @classmethod
    def describe(cls, version):
        component_descriptions = "\n".join(
                ["%s: %s" % (key, value) for key, value in cls.description[version]['components'].iteritems()])

        return "Version %s. Supported until %s.\nComponents available in this version are:\n%s" % (
            version,
            cls.end_of_support_for(version),
            component_descriptions
        )

    @classmethod
    def get_all(cls):
        return sorted(cls.description.keys(), reverse=True)

    @classmethod
    def end_of_support_for(cls, version):
        return cls.description[version]['release'] + relativedelta(months=12)
