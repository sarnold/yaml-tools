import pytest

in_xml = """\
<?xml version="1.0"?>
<mavlink>
  <include>common.xml</include>
  <version>3</version>
  <enums>
    </enums>
  <messages>
    <!-- Messages specifically designated for the Paparazzi autopilot -->
    <message id="180" name="SCRIPT_ITEM">
      <description>Message encoding a mission script item. This message is emitted upon a request for the next script item.</description>
      <field type="uint8_t" name="target_system">System ID</field>
      <field type="uint8_t" name="target_component">Component ID</field>
      <field type="uint16_t" name="seq">Sequence</field>
      <field type="char[50]" name="name">The name of the mission script, NULL terminated.</field>
    </message>
    <message id="181" name="SCRIPT_REQUEST">
      <description>Request script item with the sequence number seq. The response of the system to this message should be a SCRIPT_ITEM message.</description>
      <field type="uint8_t" name="target_system">System ID</field>
      <field type="uint8_t" name="target_component">Component ID</field>
      <field type="uint16_t" name="seq">Sequence</field>
    </message>
    <message id="182" name="SCRIPT_REQUEST_LIST">
      <description>Request the overall list of mission items from the system/component.</description>
      <field type="uint8_t" name="target_system">System ID</field>
      <field type="uint8_t" name="target_component">Component ID</field>
    </message>
    <message id="183" name="SCRIPT_COUNT">
      <description>This message is emitted as response to SCRIPT_REQUEST_LIST by the MAV to get the number of mission scripts.</description>
      <field type="uint8_t" name="target_system">System ID</field>
      <field type="uint8_t" name="target_component">Component ID</field>
      <field type="uint16_t" name="count">Number of script items in the sequence</field>
    </message>
    <message id="184" name="SCRIPT_CURRENT">
      <description>This message informs about the currently active SCRIPT.</description>
      <field type="uint16_t" name="seq">Active Sequence</field>
    </message>
  </messages>
</mavlink>
"""

out_yml = """\
mavlink:
  include: common.xml
  version: '3'
  enums:
  messages:
    '#comment': Messages specifically designated for the Paparazzi autopilot
    message:
      - '@id': '180'
        '@name': SCRIPT_ITEM
        description: Message encoding a mission script item. This message is emitted
          upon a request for the next script item.
        field:
          - '@type': uint8_t
            '@name': target_system
            '#text': System ID
          - '@type': uint8_t
            '@name': target_component
            '#text': Component ID
          - '@type': uint16_t
            '@name': seq
            '#text': Sequence
          - '@type': char[50]
            '@name': name
            '#text': The name of the mission script, NULL terminated.
      - '@id': '181'
        '@name': SCRIPT_REQUEST
        description: Request script item with the sequence number seq. The response
          of the system to this message should be a SCRIPT_ITEM message.
        field:
          - '@type': uint8_t
            '@name': target_system
            '#text': System ID
          - '@type': uint8_t
            '@name': target_component
            '#text': Component ID
          - '@type': uint16_t
            '@name': seq
            '#text': Sequence
      - '@id': '182'
        '@name': SCRIPT_REQUEST_LIST
        description: Request the overall list of mission items from the system/component.
        field:
          - '@type': uint8_t
            '@name': target_system
            '#text': System ID
          - '@type': uint8_t
            '@name': target_component
            '#text': Component ID
      - '@id': '183'
        '@name': SCRIPT_COUNT
        description: This message is emitted as response to SCRIPT_REQUEST_LIST by
          the MAV to get the number of mission scripts.
        field:
          - '@type': uint8_t
            '@name': target_system
            '#text': System ID
          - '@type': uint8_t
            '@name': target_component
            '#text': Component ID
          - '@type': uint16_t
            '@name': count
            '#text': Number of script items in the sequence
      - '@id': '184'
        '@name': SCRIPT_CURRENT
        description: This message informs about the currently active SCRIPT.
        field:
          '@type': uint16_t
          '@name': seq
          '#text': Active Sequence
"""


@pytest.fixture(scope="session")
def xml_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "in.xml"
    fn.write_text(in_xml, encoding="utf-8")
    return fn


@pytest.fixture(scope="session")
def yml_file(tmp_path_factory):
    fn = tmp_path_factory.mktemp("data") / "out.yml"
    fn.write_text(out_yml, encoding="utf-8")
    return fn
