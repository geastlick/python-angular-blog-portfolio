import { NgModule } from '@angular/core';
import { Routes, RouterModule } from '@angular/router';
import { BlogComponent } from './components/blog/blog.component';
import { PopularAuthorsComponent } from './components/popular-authors/popular-authors.component';
import { PopularBlogsComponent } from './components/popular-blogs/popular-blogs.component';


const routes: Routes = [
    { path: '', pathMatch: 'full', component: PopularBlogsComponent },
    { path: 'blogs/popular', component: PopularBlogsComponent },
    { path: 'authors/popular', component: PopularAuthorsComponent },
    { path: 'blogs/:id', component: BlogComponent },
];

@NgModule({
  imports: [RouterModule.forRoot(routes, { relativeLinkResolution: 'legacy' })],
  exports: [RouterModule]
})
export class AppRoutingModule { }
