from loader import load_catalog


class CatalogIndex:
    def __init__(self):
        self.catalog = load_catalog()

    def search_by_keyword(self, keyword):
        keyword = keyword.lower()
        results = []

        for item in self.catalog:
            name = item.get("name", "").lower()
            description = item.get("description", "").lower()

            if keyword in name or keyword in description:
                results.append(item)

        return results


if __name__ == "__main__":
    index = CatalogIndex()
    matches = index.search_by_keyword("python")

    print(f"Found {len(matches)} matches")

    for match in matches[:5]:
        print("-", match["name"])