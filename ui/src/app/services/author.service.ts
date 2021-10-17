import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from './http-error-handler.service';
import { Author } from '../interfaces/author';

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

    popular(): Observable<[Author]> {
        return this.http.get<[Author]>(this.apiUrl + '/popular', httpOptions)
        .pipe(
            catchError(this.handleError('self', <[Author]>{}))
        );
      }
}
