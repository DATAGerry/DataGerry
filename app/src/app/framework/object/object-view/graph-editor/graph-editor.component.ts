import { Component, Input, OnInit } from '@angular/core';
import {
  GraphRespWithRoot,
  GraphRespChildren,
  GraphRespParents,
} from 'src/app/framework/models/ci-explorer.model';
import { CiExplorerService } from 'src/app/framework/services/ci-explorer.service';

@Component({
  selector: 'app-graph-editor',
  templateUrl: './graph-editor.component.html',
})
export class GraphEditorComponent implements OnInit {
  @Input() rootNodeId: number;

  rootId  = null;
  childId = 2;
  parentId = 4;

  constructor(private ci: CiExplorerService) {}

  ngOnInit(): void {
    this.rootId = this.rootNodeId;

    this.loadRoot();
  }

  loadRoot(): void {
    this.ci.loadWithRoot(this.rootId).subscribe({
      next: (resp: GraphRespWithRoot) =>
        console.log('WITH_ROOT →', resp),
      error: err => console.error('WITH_ROOT error', err),
    });
  }

  expandChild(): void {
    this.ci.expandChild(this.childId).subscribe({
      next: (resp: GraphRespChildren) =>
        console.log('CHILD →', resp),
      error: err => console.error('CHILD error', err),
    });
  }

  expandParent(): void {
    this.ci.expandParent(this.parentId).subscribe({
      next: (resp: GraphRespParents) =>
        console.log('PARENT →', resp),
      error: err => console.error('PARENT error', err),
    });
  }
}
