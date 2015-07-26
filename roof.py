import bpy
import math
import operator
import mathutils
from mathutils import Matrix, Vector


# Bounding Box Mesh
class iRoof (bpy.types.Operator):
    """Roof Tile Work in Progress"""
    bl_idname = "object.isar_tile"
    bl_label = "iSar Tile"
    bl_options = {'REGISTER', 'UNDO'}

    # Make a class with the method below
    @classmethod
    def poll(cls, context):
        '''Available with selected objects'''
        if len(context.selected_objects) == 0:
            return False
        return True

    def execute(self, context):

        '''Get Tile by context object
        tile = bpy.data.objects['Tile']
        verts_tl = [v.co.to_tuple() for v in tile.data.vertices]
        polys_tl = [tuple(v for v in p.vertices) for p in tile.data.polygons]
        '''
        # Portoghese Tile
        verts_tl = [(0.0, 0.012, 0.0), (0.0, 0.0123, -0.0061), (0.0, 0.0131, -0.0116), (0.0, 0.0144, -0.0166), (0.0, 0.0162, -0.0211), (0.0, 0.0186, -0.0251), (0.0, 0.0215, -0.0285), (0.0, 0.0249, -0.0314), (0.0, 0.0289, -0.0338), (0.0, 0.0334, -0.0356), (0.0, 0.0384, -0.0369), (0.0, 0.0439, -0.0377), (0.0, 0.05, -0.038), (0.0, 0.0561, -0.0377), (0.0, 0.0616, -0.0369), (0.0, 0.0666, -0.0356), (0.0, 0.0711, -0.0338), (0.0, 0.0751, -0.0314), (0.0, 0.0785, -0.0285), (0.0, 0.0814, -0.0251), (0.0, 0.0838, -0.0211), (0.0, 0.0856, -0.0166), (0.0, 0.0869, -0.0116), (0.0, 0.0877, -0.0061), (0.0, 0.088, 0.0), (0.0, 0.0, 0.0), (0.0, 0.1, 0.0), (0.0, 0.0997, -0.008), (0.0, 0.0986, -0.0153), (0.0, 0.0969, -0.0219), (0.0, 0.0944, -0.0278), (0.0, 0.0913, -0.033), (0.0, 0.0875, -0.0375), (0.0, 0.083, -0.0413), (0.0, 0.0778, -0.0444), (0.0, 0.0719, -0.0469), (0.0, 0.0653, -0.0486), (0.0, 0.058, -0.0497), (0.0, 0.05, -0.05), (0.0, 0.042, -0.0497), (0.0, 0.0347, -0.0486), (0.0, 0.0281, -0.0469), (0.0, 0.0222, -0.0444), (0.0, 0.017, -0.0413), (0.0, 0.0125, -0.0375), (0.0, 0.0087, -0.033), (0.0, 0.0056, -0.0278), (0.0, 0.0031, -0.0219), (0.0, 0.0014, -0.0153), (0.0, 0.0003, -0.008), (-0.45, 0.098, 0.03), (-0.45, 0.0977, 0.0223), (-0.45, 0.0967, 0.0153), (-0.45, 0.095, 0.009), (-0.45, 0.0927, 0.0033), (-0.45, 0.0897, -0.0017), (-0.45, 0.086, -0.006), (-0.45, 0.0817, -0.0097), (-0.45, 0.0767, -0.0127), (-0.45, 0.071, -0.015), (-0.45, 0.0647, -0.0167), (-0.45, 0.0577, -0.0177), (-0.45, 0.05, -0.018), (-0.45, 0.0423, -0.0177), (-0.45, 0.0353, -0.0167), (-0.45, 0.029, -0.015), (-0.45, 0.0233, -0.0127), (-0.45, 0.0183, -0.0097), (-0.45, 0.014, -0.006), (-0.45, 0.0103, -0.0017), (-0.45, 0.0073, 0.0033), (-0.45, 0.005, 0.009), (-0.45, 0.0033, 0.0153), (-0.45, 0.0023, 0.0223), (-0.45, -0.01, 0.03), (-0.45, -0.0096, 0.0204), (-0.45, -0.0083, 0.0117), (-0.45, -0.0062, 0.0037), (-0.45, -0.0033, -0.0033), (-0.45, 0.0004, -0.0096), (-0.45, 0.005, -0.015), (-0.45, 0.0104, -0.0196), (-0.45, 0.0167, -0.0233), (-0.45, 0.0237, -0.0263), (-0.45, 0.0317, -0.0283), (-0.45, 0.0404, -0.0296), (-0.45, 0.05, -0.03), (-0.45, 0.0596, -0.0296), (-0.45, 0.0683, -0.0283), (-0.45, 0.0763, -0.0263), (-0.45, 0.0833, -0.0233), (-0.45, 0.0896, -0.0196), (-0.45, 0.095, -0.015), (-0.45, 0.0996, -0.0096), (-0.45, 0.1033, -0.0033), (-0.45, 0.1063, 0.0037), (-0.45, 0.1083, 0.0117), (-0.45, 0.1096, 0.0204), (-0.45, 0.11, 0.03), (-0.45, 0.002, 0.03), (-0.45, 0.163, 0.005), (-0.45, 0.1627, 0.0111), (-0.45, 0.1619, 0.0166), (-0.45, 0.1606, 0.0216), (-0.45, 0.1588, 0.0261), (-0.45, 0.1564, 0.0301), (-0.45, 0.1535, 0.0335), (-0.45, 0.1501, 0.0364), (-0.45, 0.1461, 0.0388), (-0.45, 0.1416, 0.0406), (-0.45, 0.1366, 0.0419), (-0.45, 0.1311, 0.0427), (-0.45, 0.125, 0.043), (-0.45, 0.1189, 0.0427), (-0.45, 0.1134, 0.0419), (-0.45, 0.1084, 0.0406), (-0.45, 0.1039, 0.0388), (-0.45, 0.0999, 0.0364), (-0.45, 0.0965, 0.0335), (-0.45, 0.0936, 0.0301), (-0.45, 0.0912, 0.0261), (-0.45, 0.0894, 0.0216), (-0.45, 0.0881, 0.0166), (-0.45, 0.0873, 0.0111), (-0.45, 0.087, 0.005), (-0.45, 0.175, 0.005), (-0.45, 0.075, 0.005), (-0.45, 0.0753, 0.013), (-0.45, 0.0764, 0.0203), (-0.45, 0.0781, 0.0269), (-0.45, 0.0806, 0.0328), (-0.45, 0.0837, 0.038), (-0.45, 0.0875, 0.0425), (-0.45, 0.092, 0.0463), (-0.45, 0.0972, 0.0494), (-0.45, 0.1031, 0.0519), (-0.45, 0.1097, 0.0536), (-0.45, 0.117, 0.0547), (-0.45, 0.125, 0.055), (-0.45, 0.133, 0.0547), (-0.45, 0.1403, 0.0536), (-0.45, 0.1469, 0.0519), (-0.45, 0.1528, 0.0494), (-0.45, 0.158, 0.0463), (-0.45, 0.1625, 0.0425), (-0.45, 0.1663, 0.038), (-0.45, 0.1694, 0.0328), (-0.45, 0.1719, 0.0269), (-0.45, 0.1736, 0.0203), (-0.45, 0.1747, 0.013), (0.0, 0.077, -0.025), (0.0, 0.0773, -0.0173), (0.0, 0.0783, -0.0103), (0.0, 0.08, -0.004), (0.0, 0.0823, 0.0017), (0.0, 0.0853, 0.0067), (0.0, 0.089, 0.011), (0.0, 0.0933, 0.0147), (0.0, 0.0983, 0.0177), (0.0, 0.104, 0.02), (0.0, 0.1103, 0.0217), (0.0, 0.1173, 0.0227), (0.0, 0.125, 0.023), (0.0, 0.1327, 0.0227), (0.0, 0.1397, 0.0217), (0.0, 0.146, 0.02), (0.0, 0.1517, 0.0177), (0.0, 0.1567, 0.0147), (0.0, 0.161, 0.011), (0.0, 0.1647, 0.0067), (0.0, 0.1677, 0.0017), (0.0, 0.17, -0.004), (0.0, 0.1717, -0.0103), (0.0, 0.1727, -0.0173), (0.0, 0.185, -0.025), (0.0, 0.1846, -0.0154), (0.0, 0.1833, -0.0067), (0.0, 0.1813, 0.0012), (0.0, 0.1783, 0.0083), (0.0, 0.1746, 0.0146), (0.0, 0.17, 0.02), (0.0, 0.1646, 0.0246), (0.0, 0.1583, 0.0283), (0.0, 0.1513, 0.0312), (0.0, 0.1433, 0.0333), (0.0, 0.1346, 0.0346), (0.0, 0.125, 0.035), (0.0, 0.1154, 0.0346), (0.0, 0.1067, 0.0333), (0.0, 0.0988, 0.0312), (0.0, 0.0917, 0.0283), (0.0, 0.0854, 0.0246), (0.0, 0.08, 0.02), (0.0, 0.0754, 0.0146), (0.0, 0.0717, 0.0083), (0.0, 0.0688, 0.0012), (0.0, 0.0667, -0.0067), (0.0, 0.0654, -0.0154), (0.0, 0.065, -0.025), (0.0, 0.173, -0.025)]
        polys_tl = [(50, 98, 26, 24), (74, 25, 49, 75), (48, 76, 75, 49), (47, 77, 76, 48), (46, 78, 77, 47), (45, 79, 78, 46), (44, 80, 79, 45), (43, 81, 80, 44), (42, 82, 81, 43), (41, 83, 82, 42), (40, 84, 83, 41), (39, 85, 84, 40), (38, 86, 85, 39), (37, 87, 86, 38), (36, 88, 87, 37), (35, 89, 88, 36), (34, 90, 89, 35), (33, 91, 90, 34), (32, 92, 91, 33), (31, 93, 92, 32), (30, 94, 93, 31), (29, 95, 94, 30), (28, 96, 95, 29), (27, 97, 96, 28), (26, 98, 97, 27), (0, 25, 74, 99), (0, 99, 73, 1), (1, 73, 72, 2), (2, 72, 71, 3), (3, 71, 70, 4), (4, 70, 69, 5), (5, 69, 68, 6), (6, 68, 67, 7), (7, 67, 66, 8), (8, 66, 65, 9), (9, 65, 64, 10), (10, 64, 63, 11), (11, 63, 62, 12), (12, 62, 61, 13), (13, 61, 60, 14), (14, 60, 59, 15), (15, 59, 58, 16), (16, 58, 57, 17), (17, 57, 56, 18), (18, 56, 55, 19), (19, 55, 54, 20), (20, 54, 53, 21), (21, 53, 52, 22), (22, 52, 51, 23), (23, 51, 50, 24), (0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 26, 27, 28, 29, 30, 31, 32, 33, 34, 35, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 25), (50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 99, 74, 75, 76, 77, 78, 79, 80, 81, 82, 83, 84, 85, 86, 87, 88, 89, 90, 91, 92, 93, 94, 95, 96, 97, 98), (150, 124, 126, 198), (174, 175, 149, 125), (148, 149, 175, 176), (147, 148, 176, 177), (146, 147, 177, 178), (145, 146, 178, 179), (144, 145, 179, 180), (143, 144,180, 181), (142, 143, 181, 182), (141, 142, 182, 183), (140, 141, 183, 184), (139, 140, 184, 185), (138, 139, 185, 186), (137, 138, 186, 187), (136, 137, 187, 188), (135, 136, 188, 189), (134, 135, 189, 190), (133, 134, 190, 191), (132, 133, 191, 192), (131, 132, 192, 193), (130, 131, 193, 194), (129, 130, 194, 195), (128, 129, 195, 196), (127, 128, 196, 197), (126, 127, 197, 198), (100, 199, 174, 125), (100, 101, 173, 199), (101, 102, 172, 173), (102, 103, 171, 172), (103, 104, 170, 171), (104, 105, 169, 170), (105, 106, 168, 169), (106, 107, 167, 168), (107, 108, 166, 167), (108, 109, 165, 166), (109, 110, 164, 165), (110, 111, 163, 164), (111, 112, 162, 163), (112, 113, 161, 162), (113, 114, 160, 161), (114, 115, 159, 160), (115, 116, 158, 159), (116, 117, 157, 158), (117, 118, 156, 157), (118, 119, 155, 156), (119, 120, 154, 155), (120, 121, 153, 154), (121, 122, 152, 153), (122, 123, 151, 152), (123, 124, 150, 151), (150, 198, 197, 196, 195, 194, 193, 192, 191, 190, 189, 188, 187, 186, 185, 184, 183, 182, 181, 180, 179, 178, 177, 176, 175, 174, 199, 173, 172, 171, 170, 169, 168, 167, 166, 165, 164, 163, 162, 161, 160, 159, 158, 157, 156, 155, 154, 153, 152, 151), (100, 125, 149, 148, 147, 146, 145, 144, 143, 142, 141, 140, 139, 138, 137, 136, 135, 134, 133, 132, 131, 130, 129, 128, 127, 126, 124, 123, 122, 121, 120, 119, 118, 117, 116, 115, 114, 113, 112, 111, 110, 109, 108, 107, 106, 105, 104, 103, 102, 101)]

        def iSarMatrix(a0, a1, b0, b1, src_name, dst_name):
            """Apply matrix from source polygon objects to destination objects

            :param a0: vertex Ridge
            :param a1: vertex Ridge
            :param b0: vertex Rafter
            :param b1: vertex Rafter
            :type x0, x1, y0, y1: Vector
            :param src_name: source object name
            :param dst_name: destination object name
            :type src_name, dst_name: str or unicode
            :returns:
            :rtype:
            """
            # Select object by name
            bpy.ops.object.select_all(action='DESELECT')
            bpy.ops.object.select_pattern(pattern=src_name, case_sensitive=False, extend=True)
            # Get vertices intersection point
            int = mathutils.geometry.intersect_line_line(a0, a1, b0, b1)
            # Get vertices intersection point when edges are not perfectly planar
            int_vertex = (int[0] + int[1]) / 2
            # Get first axis
            ax = (a0 - int_vertex).normalized()
            # Get third axis by crossing product of the first axis and the second edge
            az = (ax.cross(b0 - int_vertex)).normalized()
            # Get second axis by crossing product of the first and the third ones
            ay = (az.cross(ax)).normalized()
            # Create matrix by axis vectors
            mat_src = Matrix((ax, ay, az))
            # Transpose vectors in cols instead of rows
            mat_src.transpose()
            '''
            # Add translation component to source matrix
            mat_src = mat_src.to_4x4()
            mat_src.translation = int_vertex
            # Get destination object
            dst = bpy.data.objects[dst_name]
            # Add translation component to destination matrix
            dst.matrix_basis = mat_src
            # TODO Rotate Tile
            # TODO Translate Tile
            '''

            # TODO Choose between 90 and 270 degree in tab options
            # Set rotation
            mat_dst_rot = Matrix.Rotation(math.radians(90.0), 4, 'Z')
            # Get destination object
            dst = bpy.data.objects[dst_name]
            # Add translation component to destination matrix
            dst.matrix_basis = Matrix.Translation(var[0]) * mat_src.to_4x4()
            # Add rotation component to destination matrix
            dst.matrix_basis = dst.matrix_basis * mat_dst_rot

        def iSarAddEdges(src_name):
            """Add lower & higher edges"""
            src = bpy.data.objects[src_name]
            # Deselect all
            bpy.ops.object.select_all(action='DESELECT')
            # Select the source object
            bpy.data.objects[src_name].select = True
            # Get source plane matrix
            mat_src = src.matrix_world                                  # Matrix world
            # Check pitch rotation comparing the object matrix with an identitiy matrix
            if (mat_src.to_3x3() == Matrix.Scale(1, 3)):
                print('The plane was horizontal: there wouldn\'t be any higher edge if I wouldn\'t have rotate it!')
                # Rotate plane when it lays on floor
                bpy.ops.transform.rotate(value=math.radians(45), axis=(1, 1, 1), constraint_axis=(False, False, False), constraint_orientation='GLOBAL', mirror=False, proportional='DISABLED', proportional_edit_falloff='SMOOTH', proportional_size=1)

            # List vertices of the source plane
            l = []
            # Dict z components vertex and indices
            d = {}
            for i in src.data.vertices:
                # Get world vertex
                v = mat_src * i.co
                # Get keys and values from third components vertex and iterations
                d[v[2]] = len(d)
                l.append(v)
            # TODO Sort verts by indices instead of height
            s = sorted(d.items(), key=operator.itemgetter(0))
            # Get first highest vertex index
            hg1 = s[-1][1]
            # Get second highest vertex index
            hg2 = s[-2][1]
            # Get first lowest vertex index
            lw1 = s[0][1]
            # Get second lowest vertex index
            lw2 = s[1][1]

            # Get higher vertices
            verts_hg = [(l[hg1][0],l[hg1][1],l[hg1][2]), (l[hg2][0],l[hg2][1],l[hg2][2])]
            edges_hg = [(0, 1)]
            # Get higher vertex location
            ver_loc = Vector((l[hg1][0],l[hg1][1],l[hg1][2]))
            # Get edge magnitude
            edg_mgt = math.sqrt( (verts_hg[0][0] - verts_hg[1][0])**2 + (verts_hg[0][1] - verts_hg[1][1])**2 + (verts_hg[0][2] - verts_hg[1][2])**2)

            # Get lower vertices
            verts_lw = [(l[lw1][0],l[lw1][1],l[lw1][2]), (l[lw2][0],l[lw2][1],l[lw2][2])]
            edges_lw = [(0, 1)]

            # Create Ridge edge
            mesh_data = bpy.data.meshes.new("isar_edge_data")
            mesh_data.from_pydata(verts_hg, edges_hg, [])
            mesh_data.update()
            obj = bpy.data.objects.new("Ridge", mesh_data)
            scene = bpy.context.scene
            scene.objects.link(obj)
            bpy.ops.object.select_all(action='TOGGLE')                  # Deselect all
            obj.select = True                                           # Select mesh data
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            # Create Gutter edge
            mesh_data = bpy.data.meshes.new("isar_edge_data")
            mesh_data.from_pydata(verts_lw, edges_lw, [])
            mesh_data.update()
            obj = bpy.data.objects.new("Gutter", mesh_data)
            scene = bpy.context.scene
            scene.objects.link(obj)
            bpy.ops.object.select_all(action='TOGGLE')                  # Deselect all
            obj.select = True                                           # Select mesh data
            bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY')

            # Select object by name
            bpy.ops.object.select_all(action='DESELECT')
            return ver_loc, edg_mgt

        def iSarAddPerpEdge(edg_name):
            '''Get perpendicular edge'''
            # Get Ridge edge world location
            pln = bpy.data.objects[edg_name]
            mat_pln = pln.matrix_world
            # Get Ridge edge axis z from matrix
            axis_dst = (mat_src[0][2], mat_src[1][2], mat_src[2][2])
            # Get rotation value
            val_dst = math.radians(90)
            # Select Ridge
            bpy.data.objects[edg_name].select = True

            # Duplicate Ridge as Rafter
            mesh = bpy.data.meshes.new('Rafter')
            rft = bpy.data.objects.new('Rafter', mesh)
            rft.data = pln.data.copy()
            rft.scale = pln.scale
            rft.location = pln.location
            # Link new object to the given scene
            scene.objects.link(rft)
            # Select Rafter
            rft.select = True
            # Deselect Ridge
            bpy.data.objects[edg_name].select = False
            # Rotate edge
            bpy.ops.transform.rotate(value=val_dst, axis=axis_dst)

        #src = bpy.context.selected_objects
        for src in bpy.context.selected_objects:
            if bpy.data.objects.get(src.name +' Tile') is None:

                mat_src = src.matrix_world
                scene = bpy.context.scene

                ###################################################################################################### Add edges
                iSarAddEdges(src.name)

                var = iSarAddEdges(src.name)
                print(var)


                # TODO Choose by tab edg name Ridge or Gutter
                edg_name = 'Ridge' # Ridge or Gutter
                ######################################################################################### Add perpendicular edge
                iSarAddPerpEdge(edg_name)
                # Get Rafter matrix
                rft = bpy.data.objects['Rafter']
                mat_rft = rft.matrix_world
                # Get Purlin matrix
                pln = bpy.data.objects[edg_name]
                mat_pln = pln.matrix_world

                # TODO Improve code #################################################################### Get vertices from edges
                for item in bpy.data.objects:
                    if item.name == edg_name:
                        edg_pln = [mat_pln * vertex.co for vertex in item.data.vertices]
                        a0 = edg_pln[0]
                        a1 = edg_pln[1]
                    elif item.name == 'Rafter':
                        edg_rft = [mat_rft * vertex.co for vertex in item.data.vertices]
                        b0 = edg_rft[0]
                        b1 = edg_rft[1]

                ####################################################################### Apply matrix edges to destination matrix
                # Define destination objects
                bpy.ops.object.select_all(action='DESELECT')
                # Add empty
                #bpy.ops.object.empty_add(type='PLAIN_AXES')
                #dst = bpy.context.selected_objects[0]
                # Add roof tile object from vertices and polygons
                mesh_data = bpy.data.meshes.new("Portoghese Tile")
                mesh_data.from_pydata(verts_tl, [], polys_tl)
                mesh_data.update()
                dst = bpy.data.objects.new(src.name +' Tile', mesh_data)
                scene.objects.link(dst)
                bpy.ops.object.select_all(action='TOGGLE')          # Deselect all
                dst.select = True                                   # Select mesh data
                # Get destination object name
                dst_name = dst.name
                print(dst_name)

                # Define source object
                src_name = src.name
                mat_src = src.matrix_world
                vec_src = [mat_src * v.co for v in src.data.vertices]
                '''Check there are more than 3 verts
                if len(vec_src) > 3:
                    # TODO Get higher edge
                elif len(vec_src) == 3:
                    # TODO Get lower edge instead of higher edge
                else:
                    print('Wath the heck!')
                    # Delete destination object
                    bpy.ops.object.delete()
                    break
                '''
                ####################################################################### Apply matrix edges to destination matrix
                iSarMatrix(a0, a1, b0, b1, src_name, dst_name)

                ################################################################################################### Remove edges
                bpy.ops.object.select_all(action='DESELECT')

                for ob in scene.objects:
                    if ob.name.startswith("Ridge") or ob.name.startswith("Rafter") or ob.name.startswith("Gutter"):
                        ob.select = True
                    else:
                        ob.select = False
                    bpy.ops.object.delete()

        ################################################################################################################## Array
        # Select Tile
        bpy.data.objects[src_name +' Tile'].select = True
        # Active Tile
        bpy.context.scene.objects.active = dst
        # Get Ridge lenght and Rafter lenght
        ridge_length = var[1]
        # Ridge array
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array"].relative_offset_displace[1] = 0.75
        bpy.context.object.modifiers["Array"].fit_type = 'FIT_LENGTH'
        bpy.context.object.modifiers["Array"].fit_length = ridge_length
        # TODO Rafter array
        '''Rafter array
        rafter_length =
        bpy.ops.object.modifier_add(type='ARRAY')
        bpy.context.object.modifiers["Array.001"].fit_type = 'FIT_LENGTH'
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[0] = 0
        bpy.context.object.modifiers["Array.001"].relative_offset_displace[1] = 0.8
        bpy.context.object.modifiers["Array.001"].fit_length = rafter_length
        '''
        return {'FINISHED'}

