import { Author } from "./author";

export interface AuthorPaginated {
    count_all_authors: number,
    authors: [Author]
}
