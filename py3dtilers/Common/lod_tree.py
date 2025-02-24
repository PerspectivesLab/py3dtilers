from ..Common import GeometryTree, GeometryNode, Lod1Node, LoaNode, Groups


class LodTree(GeometryTree):
    """
    The LodTree contains the root node(s) of the LOD hierarchy and the centroid of the whole tileset
    """

    def __init__(self, feature_list, create_lod1=False, create_loa=False, polygons_path=None, with_texture=False, kd_tree_max=500, geometric_errors=[None, None, None]):
        """
        LodTree takes an instance of FeatureList (which contains a collection of Feature) and creates nodes.
        In order to reduce the number of .b3dm, it also distributes the features into a list of Group.
        A Group contains features and an optional polygon that will be used for LoaNodes.
        """
        root_nodes = list()

        groups = self.group_features(feature_list, polygons_path, kd_tree_max)

        for group in groups:
            node = GeometryNode(group.feature_list, geometric_errors[0], with_texture)
            root_node = node
            if create_lod1:
                lod1_node = Lod1Node(node, geometric_errors[1])
                lod1_node.add_child_node(root_node)
                root_node = lod1_node
            if create_loa:
                loa_node = LoaNode(node, geometric_errors[2], group.polygons)
                loa_node.add_child_node(root_node)
                root_node = loa_node

            root_nodes.append(root_node)

        super().__init__(root_nodes)

    def group_features(self, feature_list, polygons_path=None, kd_tree_max=500):
        """
        Distribute feature_list into groups to reduce the number of tiles.
        :param feature_list: a FeatureList to distribute into groups.
        :param polygons_path: a path to the file(s) containing polygons (used for LOA creation)
        :param kd_tree_max: the maximum number of features in each list created by the kd_tree
        :return: a list of groups, each group containing features
        """
        groups = Groups(feature_list, polygons_path, kd_tree_max)
        return groups.get_groups_as_list()
