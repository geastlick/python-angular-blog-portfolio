export interface Author {
    'id': string,
    'name': string,
    'avatar': string,
    'stars_avg': number,
    'blogs': [{
        'id': number,
        'title': string,
        'blog_stars_avg': number
    }]
}
