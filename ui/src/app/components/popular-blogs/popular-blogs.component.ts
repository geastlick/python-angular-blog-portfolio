import { Component, OnInit } from '@angular/core';
import { Blog } from 'src/app/interfaces/blog';
import { BlogService } from 'src/app/services/blogs.service';

@Component({
    selector: 'app-popular-blogs',
    templateUrl: './popular-blogs.component.html',
    styleUrls: ['./popular-blogs.component.css']
})
export class PopularBlogsComponent implements OnInit {

    blogCount: number;
    blogPageSize: number = 10;
    blogPage: number = 1;
    popularBlogs: [Blog];

    constructor(private blogService: BlogService) { }

    ngOnInit(): void {
        this.blogService.popular(this.blogPageSize, this.blogPage)
            .subscribe(
                result => {
                    this.blogCount = result['count_all_blogs'];
                    this.popularBlogs = result['blogs'];
                }
            ); 
    }

    paginate(event) {
        // page is 0 indexed
        if(event.rows != this.blogPageSize) {
            this.blogPageSize = event.rows;
            this.blogPage = Math.floor(event.first / event.rows);
            this.blogService.popular(this.blogPageSize, this.blogPage).subscribe(data => {
                this.blogCount = data['count_all_blogs'];
                this.popularBlogs = data['blogs'];
            });
        } else if(event.page + 1 != this.blogPage) {
            this.blogPage = event.page + 1;
            this.blogService.popular(this.blogPageSize, this.blogPage).subscribe(data => {
                this.blogCount = data['count_all_blogs'];
                this.popularBlogs = data['blogs'];
            });
        }
    }
}
