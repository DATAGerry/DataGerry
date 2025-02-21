import { Injectable } from '@angular/core';
import { ActivatedRouteSnapshot, RouterStateSnapshot, ResolveFn } from '@angular/router';
import { Observable } from 'rxjs';
import { inject } from '@angular/core';
import { CmdbRelation } from '../models/relation.model';
import { RelationService } from '../services/relaion.service';

/* ------------------------------------------------------------------------------------------------------------------ */
// Functional Resolver for resolving a publicID to a `CmdbRelation`.
export const RelationResolver: ResolveFn<CmdbRelation> = (route: ActivatedRouteSnapshot, state: RouterStateSnapshot): 
    Observable<CmdbRelation> | Promise<CmdbRelation> | CmdbRelation => {
    const relationService = inject(RelationService);
    const publicID: number = +route.paramMap.get('publicID');
    return relationService.getRelation(publicID);
};
