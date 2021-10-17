import { Component, OnInit } from '@angular/core';
import { Author } from 'src/app/interfaces/author';
import { AuthorService } from 'src/app/services/author.service';

@Component({
  selector: 'app-popular-authors',
  templateUrl: './popular-authors.component.html',
  styleUrls: ['./popular-authors.component.css']
})
export class PopularAuthorsComponent implements OnInit {

    authorCount: number;
    authorPageSize: number = 10;
    authorPage: number = 1;
    popularAuthors: [Author];

  constructor(private authorService: AuthorService) { }

  ngOnInit(): void {
    this.authorService.popular(this.authorPageSize, this.authorPage)
    .subscribe(
        result => {
            this.authorCount = result['count_all_authors'];
            this.popularAuthors = result['authors'];
        }
    );
}


paginate(event) {
    // page is 0 indexed
    if(event.rows != this.authorPageSize) {
        this.authorPageSize = event.rows;
        this.authorPage = Math.floor(event.first / event.rows);
        this.authorService.popular(this.authorPageSize, this.authorPage).subscribe(data => {
            this.authorCount = data['count_all_authors'];
            this.popularAuthors = data['authors'];
        });
    } else if(event.page + 1 != this.authorPage) {
        this.authorPage = event.page + 1;
        this.authorService.popular(this.authorPageSize, this.authorPage).subscribe(data => {
            this.authorCount = data['count_all_authors'];
            this.popularAuthors = data['authors'];
        });
    }
}
}
