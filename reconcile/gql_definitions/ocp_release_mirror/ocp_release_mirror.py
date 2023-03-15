"""
Generated by qenerate plugin=pydantic_v1. DO NOT MODIFY MANUALLY!
"""
from collections.abc import Callable  # noqa: F401 # pylint: disable=W0611
from datetime import datetime  # noqa: F401 # pylint: disable=W0611
from enum import Enum  # noqa: F401 # pylint: disable=W0611
from typing import (  # noqa: F401 # pylint: disable=W0611
    Any,
    Optional,
    Union,
)

from pydantic import (  # noqa: F401 # pylint: disable=W0611
    BaseModel,
    Extra,
    Field,
    Json,
)

from reconcile.gql_definitions.fragments.jumphost_common_fields import (
    CommonJumphostFields,
)
from reconcile.gql_definitions.fragments.vault_secret import VaultSecret


DEFINITION = """
fragment CommonJumphostFields on ClusterJumpHost_v1 {
  hostname
  knownHosts
  user
  port
  remotePort
  identity {
    ... VaultSecret
  }
}

fragment VaultSecret on VaultSecret_v1 {
    path
    field
    version
    format
}

query OCPReleaseMirror {
  ocp_release_mirror: ocp_release_mirror_v1 {
    hiveCluster {
      name
      serverUrl
      insecureSkipTLSVerify
      jumpHost {
        ... CommonJumphostFields
      }
      managedGroups
      ocm {
        name
        url
        orgId
        accessTokenClientId
        accessTokenUrl
        accessTokenClientSecret {
          ... VaultSecret
        }
      }
      automationToken {
        ... VaultSecret
      }
      clusterAdmin
      clusterAdminAutomationToken {
        ... VaultSecret
      }
      internal
      disable {
        integrations
        e2eTests
      }
      auth {
        service
        ... on ClusterAuthGithubOrg_v1 {
          org
        }
        ... on ClusterAuthGithubOrgTeam_v1 {
          org
          team
        }
        # ... on ClusterAuthOIDC_v1 {
        # }
      }
    }
    ecrResourcesNamespace {
      name
      managedExternalResources
      externalResources {
        provider
        provisioner {
          name
        }
        ... on NamespaceTerraformProviderResourceAWS_v1 {
          resources {
            provider
            ... on NamespaceTerraformResourceECR_v1
            {
              region
              identifier
              output_resource_name
            }
          }
        }
      }
      cluster
      {
        name
        serverUrl
        automationToken
        {
          ... VaultSecret
        }
        internal
      }
    }
    quayTargetOrgs {
      name
      instance {
        name
      }
    }
    ocpReleaseEcrIdentifier
    ocpArtDevEcrIdentifier
    mirrorChannels
  }
}
"""


class ConfiguredBaseModel(BaseModel):
    class Config:
        smart_union = True
        extra = Extra.forbid


class OpenShiftClusterManagerV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    url: str = Field(..., alias="url")
    org_id: str = Field(..., alias="orgId")
    access_token_client_id: str = Field(..., alias="accessTokenClientId")
    access_token_url: str = Field(..., alias="accessTokenUrl")
    access_token_client_secret: Optional[VaultSecret] = Field(
        ..., alias="accessTokenClientSecret"
    )


class DisableClusterAutomationsV1(ConfiguredBaseModel):
    integrations: Optional[list[str]] = Field(..., alias="integrations")
    e2e_tests: Optional[list[str]] = Field(..., alias="e2eTests")


class ClusterAuthV1(ConfiguredBaseModel):
    service: str = Field(..., alias="service")


class ClusterAuthGithubOrgV1(ClusterAuthV1):
    org: str = Field(..., alias="org")


class ClusterAuthGithubOrgTeamV1(ClusterAuthV1):
    org: str = Field(..., alias="org")
    team: str = Field(..., alias="team")


class ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    server_url: str = Field(..., alias="serverUrl")
    insecure_skip_tls_verify: Optional[bool] = Field(..., alias="insecureSkipTLSVerify")
    jump_host: Optional[CommonJumphostFields] = Field(..., alias="jumpHost")
    managed_groups: Optional[list[str]] = Field(..., alias="managedGroups")
    ocm: Optional[OpenShiftClusterManagerV1] = Field(..., alias="ocm")
    automation_token: Optional[VaultSecret] = Field(..., alias="automationToken")
    cluster_admin: Optional[bool] = Field(..., alias="clusterAdmin")
    cluster_admin_automation_token: Optional[VaultSecret] = Field(
        ..., alias="clusterAdminAutomationToken"
    )
    internal: Optional[bool] = Field(..., alias="internal")
    disable: Optional[DisableClusterAutomationsV1] = Field(..., alias="disable")
    auth: list[
        Union[ClusterAuthGithubOrgTeamV1, ClusterAuthGithubOrgV1, ClusterAuthV1]
    ] = Field(..., alias="auth")


class ExternalResourcesProvisionerV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class NamespaceExternalResourceV1(ConfiguredBaseModel):
    provider: str = Field(..., alias="provider")
    provisioner: ExternalResourcesProvisionerV1 = Field(..., alias="provisioner")


class NamespaceTerraformResourceAWSV1(ConfiguredBaseModel):
    provider: str = Field(..., alias="provider")


class NamespaceTerraformResourceECRV1(NamespaceTerraformResourceAWSV1):
    region: Optional[str] = Field(..., alias="region")
    identifier: str = Field(..., alias="identifier")
    output_resource_name: Optional[str] = Field(..., alias="output_resource_name")


class NamespaceTerraformProviderResourceAWSV1(NamespaceExternalResourceV1):
    resources: list[
        Union[NamespaceTerraformResourceECRV1, NamespaceTerraformResourceAWSV1]
    ] = Field(..., alias="resources")


class NamespaceV1_ClusterV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    server_url: str = Field(..., alias="serverUrl")
    automation_token: Optional[VaultSecret] = Field(..., alias="automationToken")
    internal: Optional[bool] = Field(..., alias="internal")


class NamespaceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    managed_external_resources: Optional[bool] = Field(
        ..., alias="managedExternalResources"
    )
    external_resources: Optional[
        list[
            Union[NamespaceTerraformProviderResourceAWSV1, NamespaceExternalResourceV1]
        ]
    ] = Field(..., alias="externalResources")
    cluster: NamespaceV1_ClusterV1 = Field(..., alias="cluster")


class QuayInstanceV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")


class QuayOrgV1(ConfiguredBaseModel):
    name: str = Field(..., alias="name")
    instance: QuayInstanceV1 = Field(..., alias="instance")


class OcpReleaseMirrorV1(ConfiguredBaseModel):
    hive_cluster: ClusterV1 = Field(..., alias="hiveCluster")
    ecr_resources_namespace: NamespaceV1 = Field(..., alias="ecrResourcesNamespace")
    quay_target_orgs: list[QuayOrgV1] = Field(..., alias="quayTargetOrgs")
    ocp_release_ecr_identifier: str = Field(..., alias="ocpReleaseEcrIdentifier")
    ocp_art_dev_ecr_identifier: str = Field(..., alias="ocpArtDevEcrIdentifier")
    mirror_channels: list[str] = Field(..., alias="mirrorChannels")


class OCPReleaseMirrorQueryData(ConfiguredBaseModel):
    ocp_release_mirror: Optional[list[OcpReleaseMirrorV1]] = Field(
        ..., alias="ocp_release_mirror"
    )


def query(query_func: Callable, **kwargs: Any) -> OCPReleaseMirrorQueryData:
    """
    This is a convenience function which queries and parses the data into
    concrete types. It should be compatible with most GQL clients.
    You do not have to use it to consume the generated data classes.
    Alternatively, you can also mime and alternate the behavior
    of this function in the caller.

    Parameters:
        query_func (Callable): Function which queries your GQL Server
        kwargs: optional arguments that will be passed to the query function

    Returns:
        OCPReleaseMirrorQueryData: queried data parsed into generated classes
    """
    raw_data: dict[Any, Any] = query_func(DEFINITION, **kwargs)
    return OCPReleaseMirrorQueryData(**raw_data)