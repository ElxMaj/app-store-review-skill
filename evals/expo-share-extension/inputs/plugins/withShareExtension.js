const { withXcodeProject, withInfoPlist } = require('@expo/config-plugins');

/**
 * Adds a Share Extension target to the Xcode project.
 * Configures NSExtension plist entries for the share extension bundle.
 */
const withShareExtension = (config, { extensionBundleIdentifier, appGroupIdentifier }) => {
  config = withXcodeProject(config, async (config) => {
    const xcodeProject = config.modResults;

    const targetName = 'ShareExtension';
    const bundleId = extensionBundleIdentifier;

    // Add a new target for the Share Extension
    const target = xcodeProject.addTarget(
      targetName,
      'app_extension',
      'ShareExtension',
      bundleId
    );

    // Configure the extension build settings
    xcodeProject.addBuildProperty('SWIFT_VERSION', '5.0', 'Debug', targetName);
    xcodeProject.addBuildProperty('SWIFT_VERSION', '5.0', 'Release', targetName);
    xcodeProject.addBuildProperty(
      'CODE_SIGN_ENTITLEMENTS',
      `ShareExtension/ShareExtension.entitlements`,
      'Debug',
      targetName
    );
    xcodeProject.addBuildProperty(
      'CODE_SIGN_ENTITLEMENTS',
      `ShareExtension/ShareExtension.entitlements`,
      'Release',
      targetName
    );

    return config;
  });

  return config;
};

module.exports = withShareExtension;
