import { BlogEntry } from "./blog-entry";

export interface BlogEntryPaginated {
    "count_all_entries": number,
    "blog_entries": [BlogEntry]
}
