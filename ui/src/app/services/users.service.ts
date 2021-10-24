import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry, tap } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from './http-error-handler.service';
import { User } from '../interfaces/user';

const httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
    })
  };

@Injectable({
  providedIn: 'root'
})
export class UserService {
  private handleError: HandleError;

  loggedIn: boolean = false;
  loggedInUser: User = null;

  constructor(
    private http: HttpClient,
    httpErrorHandler: HttpErrorHandler) {
    this.handleError = httpErrorHandler.createHandleError('UserService');
  }

  // Following are special login/logout/register related.
  login(username: string, password: string): Observable<boolean> {
    const data: any = {username: username, password: password};
    return this.http.post<boolean>('api/login', data, httpOptions)
      .pipe(
          tap(data => { this.loggedIn = data; }),
          catchError(this.handleError('login', false))
      );
  }

  self(): Observable<User> {
    return this.http.get<User>('api/self', httpOptions)
    .pipe(
        tap(data => { this.loggedInUser = data }),
        catchError(this.handleError('self', <User>{}))
    );
  }

  logout(): Observable<boolean> {
      return this.http.get<boolean>('/api/logout', httpOptions)
        .pipe(
            tap(data => { this.loggedIn = !data; }),
            catchError(this.handleError('logout', false))
        );
  }

  register(username: string, password: string, name: string, email: string): Observable<any> {
    const data: any = {username: username, password: password, name: name, email: email};
    return this.http.post<any>('api/users', data, httpOptions)
      .pipe(
          catchError(this.handleError('login', {}))
      );
  }
}

