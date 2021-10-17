import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from './http-error-handler.service';
import { Blog } from '../interfaces/blog';
import { BlogEntry } from '../interfaces/blog-entry';

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

    popular(): Observable<[Blog]> {
        return this.http.get<[Blog]>(this.apiUrl + '/popular', httpOptions)
        .pipe(
            catchError(this.handleError('self', <[Blog]>{}))
        );
      }

      entries(id: number): Observable<[BlogEntry]> {
        return this.http.get<[BlogEntry]>(this.apiUrl + '/' + id + '/entries', httpOptions)
        .pipe(
            catchError(this.handleError('self', <[BlogEntry]>{}))
        );
      }

    }
