import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BlogComponent } from './components/blog/blog.component';
import { FollowingAuthorsComponent } from './components/following-authors/following-authors.component';
import { FollowingBlogsComponent } from './components/following-blogs/following-blogs.component';
import { FollowingRecentComponent } from './components/following-recent/following-recent.component';
import { PopularAuthorsComponent } from './components/popular-authors/popular-authors.component';
import { PopularBlogsComponent } from './components/popular-blogs/popular-blogs.component';
import { LoggedInGuardService as loggedInGuard } from './services/logged-in-guard.service';

const routes: Routes = [
    { path: '', pathMatch: 'full', component: PopularBlogsComponent },
    { path: 'blogs/popular', component: PopularBlogsComponent },
    { path: 'blogs/following', component: FollowingBlogsComponent, canActivate: [loggedInGuard] },
    { path: 'blogs/:id', component: BlogComponent },
    { path: 'authors/popular', component: PopularAuthorsComponent },
    { path: 'authors/following', component: FollowingAuthorsComponent, canActivate: [loggedInGuard] },
    { path: 'following/recent', component: FollowingRecentComponent, canActivate: [loggedInGuard] },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule],
  providers: [loggedInGuard]
})
export class AppRoutingModule {
    constructor() {}
 }
