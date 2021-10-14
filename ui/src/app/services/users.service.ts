import { Injectable } from '@angular/core';
import { HttpClient, HttpParams, HttpHeaders } from '@angular/common/http';

import { Observable, throwError } from 'rxjs';
import { catchError, retry } from 'rxjs/operators';

import { HttpErrorHandler, HandleError } from '../http-error-handler.service';

const httpOptions = {
    headers: new HttpHeaders({
      'Content-Type':  'application/json',
    })
  };

@Injectable({
  providedIn: 'root'
})
export class UserService {
  usersUrl = 'api/users';
  private handleError: HandleError;

  constructor(
    private http: HttpClient,
    httpErrorHandler: HttpErrorHandler) {
    this.handleError = httpErrorHandler.createHandleError('HeroesService');
  }

  // Following are special login/logout/register related.
  login(username: string, password: string): Observable<boolean> {
    const data: any = {username: username, password: password};
    return this.http.post<boolean>('api/login', data, httpOptions)
      .pipe(
          catchError(this.handleError('login', false))
      );
  }

  logout(): Observable<boolean> {
      return this.http.get<boolean>('/api/logout', httpOptions)
        .pipe(
            catchError(this.handleError('logout', false))
        );
  }
}
