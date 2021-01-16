from components import capacitor
from components import resistor
from partnameDecoder import resistors as resistorResolver
from partnameDecoder import capacitors as capacitorResolver


def validate(part, partname_resolver, required_fields, fields_to_check):
    def has_required_fields(part):
        for field in required_fields:
           if not part[field] or part[field] == '':
               return False
        return True

    def validateParameters(part, resolved):
        for field in fields_to_check:
            if field in resolved:
                if field in ['Capacitance']:
                    if capacitor.convert_capacitance_co_farads(part[field]) != capacitor.convert_capacitance_co_farads(resolved[field]):
                        print(resolved)
                        print(str(field) + ' ' + str(part[field]) + ' ' + resolved[field])
                        return False
                elif field in ['Resistance']:
                    if resistor.convert_resistance_to_ohms(part[field]) != resistor.convert_resistance_to_ohms(resolved[field]):
                        print(resolved)
                        print(str(field) + ' ' + str(part[field]) + ' ' + resolved[field])
                        return False
                elif field in ['Voltage']:
                    if part[field].replace('VDC', 'V') != resolved[field].replace('VDC', 'V'):
                        print(resolved)
                        print(str(field) + ' ' + str(part[field]) + ' ' + resolved[field])
                        return False
                elif part[field] != resolved[field]:
                    print(resolved)
                    print(str(field))
                    return False
        return True

    validation_status = None
    if not has_required_fields(part):
        validation_status = 'MissingParameters'

    if part['Manufacturer Part Number']:
        resolvedParameters = partname_resolver.resolve(part['Manufacturer Part Number'])
        if resolvedParameters:
            if validateParameters(part, resolvedParameters) == False:
                validation_status = 'IncorrectParameters'
        else:
            validation_status = 'PartnumberDecoderMissing'
    if validation_status:
        print('Part validation failded, status: ' + validation_status)
    return validation_status


def validate_resistor(part):
    required_fields = ['Resistance', 'Case']
    fields_to_check = ['Resistance', 'Case', 'Tolerance']
    return validate(part, resistorResolver, required_fields, fields_to_check)


def validate_capacitor(part):
    required_fields = ['Capacitance', 'Voltage', 'Case']
    fields_to_check = ['Capacitance', 'Voltage', 'Case', 'Tolerance']
    return validate(part, capacitorResolver, required_fields, fields_to_check)
