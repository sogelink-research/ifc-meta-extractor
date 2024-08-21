import ifcopenshell

from typing import Any, Dict


class IFCMetadataExtractor:
    """A class to extract metadata from an IFC file."""

    def __init__(self, input_file: str):
        """
        Initializes the IFCMetadataExtractor with the input file.

        Args:
            input_file (str): The path to the input IFC file.
        """
        self.ifc_file = ifcopenshell.open(input_file)
        self.data = {}

    def get_metadata(self) -> Dict[str, Any]:
        """
        Extracts metadata from the IFC file and returns it as a JSON object.

        Returns:
            Dict[str, Any]: The extracted metadata.
        """
        self._add_layers()
        self._add_groups()
        self._add_ifc_projects()
        return self.data

    def _get_element_properties(self, property_set) -> Dict[str, Any]:
        """Extracts properties from the property set."""
        properties = {
            'name': property_set.Name,
            'properties': []
        }
        for prop in property_set.HasProperties:
            property_value = None
            if prop.is_a('IfcPropertySingleValue') and prop.NominalValue is not None:
                property_value = str(prop.NominalValue.wrappedValue)

            properties['properties'].append({
                'name': prop.Name,
                'value': property_value
            })
        return properties

    def _get_element_quantities(self, quantity_set) -> Dict[str, Any]:
        """Extracts quantities from the quantity set."""
        quantities = {
            'name': quantity_set.Name,
            'quantities': []
        }
        for quantity in quantity_set.Quantities:
            quantity_info = {
                'name': quantity.Name,
                'value': None
            }
            for attr_name in dir(quantity):
                if attr_name.endswith('Value'):
                    quantity_info['value'] = str(getattr(quantity, attr_name))
                    break
            quantities['quantities'].append(quantity_info)
        return quantities

    def _get_element_type(self, type) -> Dict[str, str]:
        """Extracts information from the type."""
        return {'name': type.Name}

    def _get_element(self, element, parentId) -> Dict[str, Any]:
        """Extracts information from the element."""
        result = {
            'id': element.id(),
            'ifcId': element.GlobalId,
            'parentId': parentId,
            'type': str(element.is_a()),
            'name': str(element.Name),
            'properties': [],
            'quantities': [],
            'children': [],
        }
        self._add_properties_and_quantities(element, result)
        self._add_children(element, result)
        return result

    def _add_properties_and_quantities(self, element, result: Dict[str, Any]) -> None:
        """Extracts properties and quantities from the element."""
        for definition in element.IsDefinedBy:
            if definition.is_a('IfcRelDefinesByProperties'):
                related_data = definition.RelatingPropertyDefinition
                if related_data.is_a('IfcPropertySet'):
                    result['properties'].append(
                        self._get_element_properties(related_data))
                elif related_data.is_a('IfcElementQuantity'):
                    result['quantities'].append(
                        self._get_element_quantities(related_data))
            elif definition.is_a('IfcRelDefinesByType'):
                result['type'] = self._get_element_type(
                    definition.RelatingType)

    def _add_children(self, element, result: Dict[str, Any]) -> None:
        """Extracts child elements from the element."""
        if element.is_a('IfcSpatialStructureElement'):
            for rel in element.ContainsElements:
                for child in rel.RelatedElements:
                    result['children'].append(
                        self._get_element(child, result['id']))
        if element.is_a('IfcObjectDefinition'):
            for rel in element.IsDecomposedBy:
                for child in rel.RelatedObjects:
                    result['children'].append(
                        self._get_element(child, result['id']))

    def _add_layers(self) -> None:
        """Extracts IfcPresentationLayerAssignment and related elements."""
        layers = []

        for layer_assignment in self.ifc_file.by_type('IfcPresentationLayerAssignment'):
            layer_data = {
                "name": layer_assignment.Name,
                "items": []
            }

            for item in layer_assignment.AssignedItems:
                parent_product = None

                # Search through all IfcProducts to find the one that uses this shape representation
                for product in self.ifc_file.by_type('IfcProduct'):
                    if hasattr(product, 'Representation') and product.Representation is not None:
                        representations = product.Representation.Representations
                        if item in representations:
                            parent_product = product
                            break

                if parent_product:
                    # Add the parent's name and GlobalId to the layer items
                    layer_data["items"].append({
                        "name": parent_product.Name,
                        "ifcId": parent_product.GlobalId
                    })

            layers.append(layer_data)

        self.data["layers"] = layers

    def _add_groups(self) -> None:
        """Extracts IfcGroup and related elements."""
        groups = []

        for group in self.ifc_file.by_type('IfcGroup'):
            group_info = {
                "id": group.id(),
                "ifcId": group.GlobalId,
                "name": str(group.Name),
                "type": str(group.is_a()),
                "items": []
            }

            for rel in group.IsGroupedBy:
                if rel.is_a('IfcRelAssignsToGroup'):
                    for item in rel.RelatedObjects:
                        item_info = {
                            "name": str(item.Name),
                            "ifcId": item.GlobalId
                        }
                        group_info["items"].append(item_info)

            groups.append(group_info)

        self.data["groups"] = groups

    def _add_ifc_projects(self) -> None:
        """Extracts IfcProject and related elements."""
        projects = [
            self._get_element(project, -1)
            for project in self.ifc_file.by_type('IfcProject')
        ]
        self.data["projects"] = projects
