import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from './http-error-handler.service';
import { Blog } from '../interfaces/blog';

const httpOptions = {
    headers: new HttpHeaders({
        'Content-Type': 'application/json',
    })
};

@Injectable({
    providedIn: 'root'
})
export class BlogService {
    private blogsUrl = 'api/blogs';
    private handleError: HandleError;

    constructor(
        private http: HttpClient,
        httpErrorHandler: HttpErrorHandler) {
        this.handleError = httpErrorHandler.createHandleError('BlogService');
    }

    popular(): Observable<[Blog]> {
        return this.http.get<[Blog]>(this.blogsUrl + '/popular', httpOptions)
        .pipe(
            catchError(this.handleError('self', <[Blog]>{}))
        );
      }

    }
