export interface MigrationOptionsModel {
  isCheckedEnvironmentVariables: boolean;
  isCheckedPublishProcessBeforeMigration: boolean;
  isCheckedCompanySettings: boolean;
  isCheckedPublishProcessPostMigration: boolean;
  isCheckedAddAndAssignDummyHubToAdmin: boolean;
  isCheckedMigrateDataStore: boolean;
  isCheckedUpdatePostHookUrl: boolean;
  isCheckedCitiesBranches: boolean;
  isCheckedGeoLocation: boolean;
  isCheckedVehicleConfiguration: boolean;
  isCheckedUsers: boolean;
}
