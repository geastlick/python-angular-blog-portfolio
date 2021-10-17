import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { Blog } from 'src/app/interfaces/blog';
import { BlogEntry } from 'src/app/interfaces/blog-entry';
import { BlogService } from 'src/app/services/blogs.service';

@Component({
    selector: 'app-blog',
    templateUrl: './blog.component.html',
    styleUrls: ['./blog.component.css']
})
export class BlogComponent implements OnInit {

    id: number;
    blog: Blog;
    entryCount: number;
    entryPageSize: number = 10;
    entryPage: number = 1;
    entries: [BlogEntry];

    constructor(private blogService: BlogService, private route: ActivatedRoute) { }

    ngOnInit(): void {
        this.route.params.subscribe(params => {
            this.id = params['id'];
            this.blogService.by_id(params['id']).subscribe(data => {
                this.blog = data;
            });
            this.blogService.entries(params['id'], this.entryPageSize, this.entryPage).subscribe(data => {
                this.entryCount = data['count_all_entries'];
                this.entries = data['blog_entries'];
            });
          });
    }

    paginate(event) {
        // page is 0 indexed
        if(event.rows != this.entryPageSize) {
            this.entryPageSize = event.rows;
            this.entryPage = Math.floor(event.first / event.rows);
            this.blogService.entries(this.id, this.entryPageSize, this.entryPage).subscribe(data => {
                this.entryCount = data['count_all_entries'];
                this.entries = data['blog_entries'];
            });
        } else if(event.page + 1 != this.entryPage) {
            this.entryPage = event.page + 1;
            this.blogService.entries(this.id, this.entryPageSize, this.entryPage).subscribe(data => {
                this.entryCount = data['count_all_entries'];
                this.entries = data['blog_entries'];
            });
        }
    }

}
