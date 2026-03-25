import math

class KDNode:
    def __init__(self, stall, left=None, right=None):
        self.stall = stall
        self.left = left
        self.right = right


class KDTree:
    def __init__(self, stalls):
        self.root = self._build(list(stalls), depth=0)

    def _build(self, stalls, depth):
        if not stalls:
            return None
        axis = depth % 2  # 0 = lat, 1 = lng
        key = 'lat' if axis == 0 else 'lng'
        stalls.sort(key=lambda s: s[key])
        mid = len(stalls) // 2
        return KDNode(
            stall=stalls[mid],
            left=self._build(stalls[:mid], depth + 1),
            right=self._build(stalls[mid + 1:], depth + 1)
        )

    def _dist(self, a, b):
        return math.sqrt((a['lat'] - b['lat']) ** 2 + (a['lng'] - b['lng']) ** 2)

    def nearest(self, query, k=3):
        best = []

        def search(node, depth):
            if node is None:
                return
            d = self._dist(query, node.stall)
            if len(best) < k:
                best.append((d, node.stall))
                best.sort(key=lambda x: x[0])
            elif d < best[-1][0]:
                best[-1] = (d, node.stall)
                best.sort(key=lambda x: x[0])

            key = 'lat' if depth % 2 == 0 else 'lng'
            diff = query[key] - node.stall[key]
            near, far = (node.left, node.right) if diff <= 0 else (node.right, node.left)
            search(near, depth + 1)
            if len(best) < k or abs(diff) < best[-1][0]:
                search(far, depth + 1)

        search(self.root, 0)
        return [{'stall': s, 'distance': round(d, 6)} for d, s in best]

    def range_query(self, query, radius):
        results = []

        def search(node, depth):
            if node is None:
                return
            d = self._dist(query, node.stall)
            if d <= radius:
                results.append({'stall': node.stall, 'distance': round(d, 6)})

            key = 'lat' if depth % 2 == 0 else 'lng'
            diff = query[key] - node.stall[key]
            near, far = (node.left, node.right) if diff <= 0 else (node.right, node.left)
            search(near, depth + 1)
            if abs(diff) <= radius:
                search(far, depth + 1)

        search(self.root, 0)
        results.sort(key=lambda r: r['distance'])
        return results
