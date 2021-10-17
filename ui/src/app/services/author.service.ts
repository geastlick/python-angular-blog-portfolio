import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from './http-error-handler.service';
import { Author } from '../interfaces/author';
import { AuthorPaginated } from '../interfaces/author-paginated';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json',
    })
};

@Injectable({
    providedIn: 'root'
})
export class AuthorService {
    private apiUrl = 'api/authors';
    private handleError: HandleError;

    constructor(
        private http: HttpClient,
        httpErrorHandler: HttpErrorHandler) {
        this.handleError = httpErrorHandler.createHandleError('BlogService');
    }

    by_id(id: number): Observable<Author> {
        return this.http.get<Author>(this.apiUrl + '/' + id, httpOptions)
            .pipe(
                catchError(this.handleError('self', <Author>{}))
            );
    }

    popular(pagesize: number = 0, page: number = 0): Observable<[AuthorPaginated]> {
        let queryParam = "";
        if (pagesize > 0) {
            queryParam += "?page_size=" + pagesize;
            if (page > 0) {
                queryParam += "&page=" + page
            }
        }
        return this.http.get<[AuthorPaginated]>(this.apiUrl + '/popular' + queryParam, httpOptions)
            .pipe(
                catchError(this.handleError('self', <[AuthorPaginated]>{}))
            );
    }
}
