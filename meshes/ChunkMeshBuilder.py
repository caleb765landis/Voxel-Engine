from settings import *
from numba import uint8

# builds mesh of chunks that only renders voxel faces that can be seen by player
# all functions use numba's just in time compiler to SIGNIFICANTLY speed up mesh building
@njit
def build_chunk_mesh(chunk_voxels, format_size, chunk_pos, world_voxels):
    # empty vector of vertex data
    # 18 is max number of vertices that could possibly be seen
    # 5 vertex attributes
    vertex_data = np.empty(CHUNK_VOL * 18 * format_size, dtype='uint8')
    index = 0

    # iterate over chunk and check if voxel is not empty
    for x in range(CHUNK_SIZE):
        for y in range(CHUNK_SIZE):
            for z in range(CHUNK_SIZE):
                voxel_id = chunk_voxels[x + CHUNK_SIZE * z + CHUNK_AREA * y]
                if not voxel_id:
                    continue

                # voxel world position
                cx, cy, cz = chunk_pos
                wx = x + cx * CHUNK_SIZE
                wy = y + cy * CHUNK_SIZE
                wz = z + cz * CHUNK_SIZE


                '''
                FACE IDs:
                0 - top
                1 - bottom
                2 - right
                3 - left
                4 - back
                5 - front
                '''

                # top face
                if is_void((x, y + 1, z), (wx, wy + 1, wz), world_voxels):
                    # format x, y, z, voxel_id, face_id
                    v0 = to_uint8(x, y + 1, z, voxel_id, 0)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 0)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 0)
                    v3 = to_uint8(x, y + 1, z + 1, voxel_id, 0)

                    # can create two mesh triangles from the formed vertex vertices
                    index = add_data(vertex_data, index, v0, v3, v2, v0, v2, v1)

                # bottom face
                if is_void((x, y - 1, z), (wx, wy - 1, wz), world_voxels):
                    # format x, y, z, voxel_id, face_id
                    v0 = to_uint8(x, y, z, voxel_id, 1)
                    v1 = to_uint8(x + 1, y, z, voxel_id, 1)
                    v2 = to_uint8(x + 1, y, z + 1, voxel_id, 1)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 1)

                    # can create two mesh triangles from the formed vertex vertices
                    index = add_data(vertex_data, index, v0, v2, v3, v0, v1, v2)

                # right face
                if is_void((x + 1, y, z), (wx + 1, wy, wz), world_voxels):
                    # format x, y, z, voxel_id, face_id
                    v0 = to_uint8(x + 1, y, z, voxel_id, 2)
                    v1 = to_uint8(x + 1, y + 1, z, voxel_id, 2)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 2)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 2)

                    # can create two mesh triangles from the formed vertex vertices
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # left face
                if is_void((x - 1, y, z), (wx - 1, wy, wz), world_voxels):
                    # format x, y, z, voxel_id, face_id
                    v0 = to_uint8(x, y, z, voxel_id, 3)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 3)
                    v2 = to_uint8(x, y + 1, z + 1, voxel_id, 3)
                    v3 = to_uint8(x, y, z + 1, voxel_id, 3)

                    # can create two mesh triangles from the formed vertex vertices
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)

                # back face
                if is_void((x, y, z - 1), (wx, wy, wz - 1), world_voxels):
                    # format x, y, z, voxel_id, face_id
                    v0 = to_uint8(x, y, z, voxel_id, 4)
                    v1 = to_uint8(x, y + 1, z, voxel_id, 4)
                    v2 = to_uint8(x + 1, y + 1, z, voxel_id, 4)
                    v3 = to_uint8(x + 1, y, z, voxel_id, 4)

                    # can create two mesh triangles from the formed vertex vertices
                    index = add_data(vertex_data, index, v0, v1, v2, v0, v2, v3)

                # front face
                if is_void((x, y, z + 1), (wx, wy, wz + 1), world_voxels):
                    # format x, y, z, voxel_id, face_id
                    v0 = to_uint8(x, y, z + 1, voxel_id, 5)
                    v1 = to_uint8(x, y + 1, z + 1, voxel_id, 5)
                    v2 = to_uint8(x + 1, y + 1, z + 1, voxel_id, 5)
                    v3 = to_uint8(x + 1, y, z + 1, voxel_id, 5)

                    # can create two mesh triangles from the formed vertex vertices
                    index = add_data(vertex_data, index, v0, v2, v1, v0, v3, v2)
    
    return vertex_data[:index + 1]

@njit
def to_uint8(x, y, z, voxel_id, face_id):
    return uint8(x), uint8(y), uint8(z), uint8(voxel_id), uint8(face_id)

@njit
def get_chunk_index(world_voxel_pos):
    wx, wy, wz = world_voxel_pos
    cx = wx // CHUNK_SIZE
    cy = wy // CHUNK_SIZE
    cz = wz // CHUNK_SIZE

    # if position is out of bounds of world, return -1
    if not (0 <= cx < WORLD_W and 0 <= cy < WORLD_H and 0 <= cz < WORLD_D):
        return -1
    
    # otherwise return calculated chunk index
    index = cx + WORLD_W * cz + WORLD_AREA * cy
    return index

# checks if voxel is empty or out of chunk's bounds
@njit
def is_void(local_voxel_pos, world_voxel_pos, world_voxels):
    chunk_index = get_chunk_index(world_voxel_pos)

    # if chunk is not out of bounds, we can access its voxels
    if chunk_index == -1:
        return False
    chunk_voxels = world_voxels[chunk_index]

    x, y, z = local_voxel_pos

    # make sure index is within bounds of this chunk's slice of the array
    voxel_index = x % CHUNK_SIZE + z % CHUNK_SIZE * CHUNK_SIZE + y % CHUNK_SIZE * CHUNK_AREA

    # if voxel exists, then it is not void, otherwise return true because it is
    if chunk_voxels[voxel_index]:
        return False
    return True

@njit
def add_data(vertex_data, index, *vertices):
    for vertex in vertices:
        for attr in vertex:
            vertex_data[index] = attr
            index += 1
    return index