graphql_query = '''
    query GetFruits($storeId: Int!, $slug: String!, $attributes: [AttributeFilter], $filters: [FieldFilter], $from: Int!, $size: Int!, $sort: InCategorySort, $in_stock: Boolean, $eshop_order: Boolean, $is_action: Boolean, $price_levels: Boolean) {
  category(storeId: $storeId, slug: $slug, inStock: $in_stock, eshopAvailability: $eshop_order, isPromo: $is_action, priceLevels: $price_levels) {
    products(attributeFilters: $attributes, from: $from, size: $size, sort: $sort, fieldFilters: $filters) {
      id
      name
      url  
      manufacturer {
        name 
      }
      stocks {
        value
        prices {
          price
          old_price
        }
      }
    }
  }
}
'''

graphql_variables = '''
{
  "storeId": 10,
  "slug": "konfety-podarochnye-nabory",
  "attributes": [],
  "filters": [
    {
      "field": "main_article",
      "value": "0"
    }
  ],
  "from": 0,
  "size": 99999999,
  "in_stock": false,
  "eshop_order": false,
  "is_action": false,
  "price_levels": false
}
'''

graphql_url = "https://api.metro-cc.ru/products-api/graph"