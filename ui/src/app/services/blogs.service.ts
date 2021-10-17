import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from './http-error-handler.service';
import { Blog } from '../interfaces/blog';
import { BlogPaginated } from '../interfaces/blog-paginated';
import { BlogEntryPaginated } from '../interfaces/blog-entry-paginated';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json',
    })
};

@Injectable({
    providedIn: 'root'
})
export class BlogService {
    private apiUrl = 'api/blogs';
    private handleError: HandleError;

    constructor(
        private http: HttpClient,
        httpErrorHandler: HttpErrorHandler) {
        this.handleError = httpErrorHandler.createHandleError('BlogService');
    }

    by_id(id: number): Observable<Blog> {
        return this.http.get<Blog>(this.apiUrl + '/' + id, httpOptions)
        .pipe(
            catchError(this.handleError('self', <Blog>{}))
        );
    }

    popular(pagesize:number = 0, page:number = 0): Observable<[BlogPaginated]> {
        let queryParam = "";
        if (pagesize > 0) {
            queryParam += "?page_size=" + pagesize;
            if (page > 0) {
                queryParam += "&page=" + page
            }
        }
        return this.http.get<[BlogPaginated]>(this.apiUrl + '/popular' + queryParam, httpOptions)
        .pipe(
            catchError(this.handleError('self', <[BlogPaginated]>{}))
        );
      }

      entries(id: number, pagesize:number = 0, page:number = 0): Observable<[BlogEntryPaginated]> {
        let queryParam = "";
        if (pagesize > 0) {
            queryParam += "?page_size=" + pagesize;
            if (page > 0) {
                queryParam += "&page=" + page
            }
        }
        return this.http.get<[BlogEntryPaginated]>(this.apiUrl + '/' + id + '/entries' + queryParam, httpOptions)
        .pipe(
            catchError(this.handleError('self', <[BlogEntryPaginated]>{}))
        );
      }

    }
