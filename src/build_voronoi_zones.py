import numpy as np

def voronoi_finite_polygons(vor, radius=None):
    """
    Reconstruct infinite Voronoi regions into finite polygons by extending ridges.
    Returns (regions, vertices). Each region is a list of vertex indices.
    """

    # Ensure only 2D Voronoi diagrams are processed
    if vor.points.shape[1] != 2:
        raise ValueError("Only 2D input supported.")
    
    
    # Create the output lists
    # new_regions: list of lists of vertex indices per cell
    new_regions = []
    # new_vertices: start with the original Voronoi vertices
    new_vertices = vor.vertices.tolist()

    # Compute the geometric center (mean) of the input points.
    # Choose a consistent outward direction when extending infinite edges.
    center = vor.points.mean(axis=0)

    # If no radius is provided, set it to a large enough value based on the data spread
    # To make radius large enough, we use the max range across axes (peak-to-peak) times 100.
    # We use it as a heuristic that makes the extension long enough to close infinite regions.
    if radius is None:
        radius = np.ptp(vor.points, axis=0).max() * 100


    # Build a map of all ridges (edges) incident to each input point.
    # vor.ridge_points: pairs of input point indices (p1, p2) that share a Voronoi edge
    # vor.ridge_vertices: matching pairs of vertex indices (v1, v2) for each ridge.
    # If a vertex index is -1, that endpoint is at infinity.
    all_ridges = {}
    for (p1, p2), (v1, v2) in zip(vor.ridge_points, vor.ridge_vertices):
        # For each point, collect tuples of neighbor point and ridge vertex indices
        all_ridges.setdefault(p1, []).append((p2, v1, v2))
        all_ridges.setdefault(p2, []).append((p1, v1, v2))

    # Construct finite regions
    # Iterate over each generator point and its region index
    for p1, region_index in enumerate(vor.point_region):
        # The region is a list of vertex indices; -1s mark infinite vertices
        region = vor.regions[region_index]

        # If region is finite (no -1) and not empty, keep it as is
        if -1 not in region and region:  # already finite
            new_regions.append(region)
            continue

        # Otherwise, reconstruct the region:
        # - Get all ridges touching p1
        ridges = all_ridges[p1]

        # - Start with the existing finite vertices in the region (exclude -1 and None)
        new_region = [v for v in region if v != -1 and v is not None]

        # For each ridge, if it has an infinite endpoint, extend it to a finite far point
        for p2, v1, v2 in ridges:
            if v1 == -1 or v2 == -1:
                # Direction along the edge between points p1 and p2 (unit vector)
                t = vor.points[p2] - vor.points[p1]
                t /= np.linalg.norm(t)

                # Normal vector n perpendicular to t. This gives us directions orthogonal to the ridge.
                n = np.array([-t[1], t[0]])

                # Midpoint of the two generator points. Used to choose extension direction.
                midpoint = (vor.points[p1] + vor.points[p2]) / 2

                # Decide which side to extend: outward from the diagram center.
                # sign(...) selects +n or -n based on the dot product.
                direction = np.sign(np.dot(midpoint - center, n)) * n

                # Take the finite endpoint of the ridge (either v1 or v2) as the base
                base = vor.vertices[[v for v in (v1, v2) if v != -1][0]]

                # Extend from base along the chosen normal direction by 'radius'
                far_point = base + direction * radius

                # Add the new vertex to the vertex list
                new_vertices.append(far_point.tolist())

                # Record its index as part of the new region
                new_region.append(len(new_vertices) - 1)

        # Order vertices counter-clockwise after collecting/creating all vertices for this region
        ## Get coordinate array for the new region vertices
        vs = np.asarray([new_vertices[v] for v in new_region])

        ## Compute centroid of the region vertices
        c = vs.mean(axis=0)

        ## Compute angles from centroid to each vertex
        angles = np.arctan2(vs[:,1] - c[1], vs[:,0] - c[0])

        ## Sort vertices by angle and use that order as the region vertex order
        new_region = [v for _, v in sorted(zip(angles, new_region))]

        ## Append the ordered region to the list
        new_regions.append(new_region)

    return new_regions, np.asarray(new_vertices)