import { Blog } from "./blog";

export interface BlogPaginated {
    'count_all_blogs': number,
    'blogs': [Blog]
}
