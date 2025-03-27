import { Injectable } from '@angular/core';

@Injectable({
  providedIn: 'root'
})
export class FilterBuilderService {

  constructor() { }

  /**
   * Builds a MongoDB-like aggregation pipeline query for text-based searching
   * on specified fields.
   * 
   * @param filterValue The text to filter by (e.g. from a search box).
   * @param fields An array of fields that should be filtered on. 
   *               Each item can describe how to handle that field
   *               (e.g., direct string, array, etc.).
   * @returns an array representing the MongoDB pipeline `$match` stage.
   * 
   * Example usage:
   *   buildFilter('foo', [
   *     { name: 'public_id', isArray: false },
   *     { name: 'categories', isArray: true },
   *   ]);
   */
  public buildFilter(
    filterValue: string,
    fields: Array<{ name: string; isArray?: boolean }>
  ): any[] {
    const query: any[] = [];

    if (!filterValue) {
      return query; // no filter
    }

    const orConditions: any[] = [];

    // Convert to string once, for safety
    const filterString = String(filterValue);

    fields.forEach(field => {
      if (field.isArray) {
        // For array fields, we often need $elemMatch with $regex
        orConditions.push({
          [field.name]: {
            $elemMatch: {
              $regex: filterString,
              $options: 'i'
            }
          }
        });
      } else {
        // Simple string field
        orConditions.push({
          [field.name]: {
            $regex: filterString,
            $options: 'i'
          }
        });
      }
    });

    // If you need $match with $or
    if (orConditions.length) {
      query.push({ $match: { $or: orConditions } });
    }

    return query;
  }
}
