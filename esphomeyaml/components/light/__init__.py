import voluptuous as vol

from esphomeyaml.automation import ACTION_REGISTRY, maybe_simple_id
from esphomeyaml.components import mqtt
import esphomeyaml.config_validation as cv
from esphomeyaml.const import CONF_ALPHA, CONF_BLUE, CONF_BRIGHTNESS, CONF_COLORS, \
    CONF_COLOR_TEMPERATURE, CONF_DEFAULT_TRANSITION_LENGTH, CONF_DURATION, CONF_EFFECT, \
    CONF_EFFECTS, CONF_EFFECT_ID, CONF_FLASH_LENGTH, CONF_GAMMA_CORRECT, CONF_GREEN, CONF_ID, \
    CONF_INTERNAL, CONF_LAMBDA, CONF_MQTT_ID, CONF_NAME, CONF_NUM_LEDS, CONF_RANDOM, CONF_RED, \
    CONF_SPEED, CONF_STATE, CONF_TRANSITION_LENGTH, CONF_UPDATE_INTERVAL, CONF_WHITE, CONF_WIDTH
from esphomeyaml.helpers import Action, Application, ArrayInitializer, Component, Nameable, \
    Pvariable, StructInitializer, TemplateArguments, add, add_job, esphomelib_ns, float_, \
    get_variable, process_lambda, setup_mqtt_component, std_string, templatable, uint32

PLATFORM_SCHEMA = cv.PLATFORM_SCHEMA.extend({

})

# Base
light_ns = esphomelib_ns.namespace('light')
LightState = light_ns.class_('LightState', Nameable, Component)
MakeLight = Application.struct('MakeLight')
LightOutput = light_ns.class_('LightOutput')
FastLEDLightOutputComponent = light_ns.class_('FastLEDLightOutputComponent', LightOutput)

# Actions
ToggleAction = light_ns.class_('ToggleAction', Action)
TurnOffAction = light_ns.class_('TurnOffAction', Action)
TurnOnAction = light_ns.class_('TurnOnAction', Action)

LightColorValues = light_ns.class_('LightColorValues')

MQTTJSONLightComponent = light_ns.class_('MQTTJSONLightComponent', mqtt.MQTTComponent)

# Effects
LightEffect = light_ns.class_('LightEffect')
RandomLightEffect = light_ns.class_('RandomLightEffect', LightEffect)
LambdaLightEffect = light_ns.class_('LambdaLightEffect', LightEffect)
StrobeLightEffect = light_ns.class_('StrobeLightEffect', LightEffect)
StrobeLightEffectColor = light_ns.class_('StrobeLightEffectColor', LightEffect)
FlickerLightEffect = light_ns.class_('FlickerLightEffect', LightEffect)
BaseFastLEDLightEffect = light_ns.class_('BaseFastLEDLightEffect', LightEffect)
FastLEDLambdaLightEffect = light_ns.class_('FastLEDLambdaLightEffect', BaseFastLEDLightEffect)
FastLEDRainbowLightEffect = light_ns.class_('FastLEDRainbowLightEffect', BaseFastLEDLightEffect)
FastLEDColorWipeEffect = light_ns.class_('FastLEDColorWipeEffect', BaseFastLEDLightEffect)
FastLEDColorWipeEffectColor = light_ns.class_('FastLEDColorWipeEffectColor', BaseFastLEDLightEffect)
FastLEDScanEffect = light_ns.class_('FastLEDScanEffect', BaseFastLEDLightEffect)
FastLEDScanEffectColor = light_ns.class_('FastLEDScanEffectColor', BaseFastLEDLightEffect)
FastLEDTwinkleEffect = light_ns.class_('FastLEDTwinkleEffect', BaseFastLEDLightEffect)
FastLEDRandomTwinkleEffect = light_ns.class_('FastLEDRandomTwinkleEffect', BaseFastLEDLightEffect)
FastLEDFireworksEffect = light_ns.class_('FastLEDFireworksEffect', BaseFastLEDLightEffect)
FastLEDFlickerEffect = light_ns.class_('FastLEDFlickerEffect', BaseFastLEDLightEffect)

CONF_STROBE = 'strobe'
CONF_FLICKER = 'flicker'
CONF_FASTLED_LAMBDA = 'fastled_lambda'
CONF_FASTLED_RAINBOW = 'fastled_rainbow'
CONF_FASTLED_COLOR_WIPE = 'fastled_color_wipe'
CONF_FASTLED_SCAN = 'fastled_scan'
CONF_FASTLED_TWINKLE = 'fastled_twinkle'
CONF_FASTLED_RANDOM_TWINKLE = 'fastled_random_twinkle'
CONF_FASTLED_FIREWORKS = 'fastled_fireworks'
CONF_FASTLED_FLICKER = 'fastled_flicker'

CONF_ADD_LED_INTERVAL = 'add_led_interval'
CONF_REVERSE = 'reverse'
CONF_MOVE_INTERVAL = 'move_interval'
CONF_TWINKLE_PROBABILITY = 'twinkle_probability'
CONF_PROGRESS_INTERVAL = 'progress_interval'
CONF_SPARK_PROBABILITY = 'spark_probability'
CONF_USE_RANDOM_COLOR = 'use_random_color'
CONF_FADE_OUT_RATE = 'fade_out_rate'
CONF_INTENSITY = 'intensity'

BINARY_EFFECTS = [CONF_LAMBDA, CONF_STROBE]
MONOCHROMATIC_EFFECTS = BINARY_EFFECTS + [CONF_FLICKER]
RGB_EFFECTS = MONOCHROMATIC_EFFECTS + [CONF_RANDOM]
FASTLED_EFFECTS = RGB_EFFECTS + [CONF_FASTLED_LAMBDA, CONF_FASTLED_RAINBOW, CONF_FASTLED_COLOR_WIPE,
                                 CONF_FASTLED_SCAN, CONF_FASTLED_TWINKLE,
                                 CONF_FASTLED_RANDOM_TWINKLE, CONF_FASTLED_FIREWORKS,
                                 CONF_FASTLED_FLICKER]

EFFECTS_SCHEMA = vol.Schema({
    vol.Optional(CONF_LAMBDA): vol.Schema({
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_LAMBDA): cv.lambda_,
        vol.Optional(CONF_UPDATE_INTERVAL, default='0ms'): cv.positive_time_period_milliseconds,
    }),
    vol.Optional(CONF_RANDOM): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(RandomLightEffect),
        vol.Optional(CONF_NAME, default="Random"): cv.string,
        vol.Optional(CONF_TRANSITION_LENGTH): cv.positive_time_period_milliseconds,
        vol.Optional(CONF_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
    }),
    vol.Optional(CONF_STROBE): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(StrobeLightEffect),
        vol.Optional(CONF_NAME, default="Strobe"): cv.string,
        vol.Optional(CONF_COLORS): vol.All(cv.ensure_list, [vol.All(vol.Schema({
            vol.Optional(CONF_STATE, default=True): cv.boolean,
            vol.Optional(CONF_BRIGHTNESS, default=1.0): cv.percentage,
            vol.Optional(CONF_RED, default=1.0): cv.percentage,
            vol.Optional(CONF_GREEN, default=1.0): cv.percentage,
            vol.Optional(CONF_BLUE, default=1.0): cv.percentage,
            vol.Optional(CONF_WHITE, default=1.0): cv.percentage,
            vol.Required(CONF_DURATION): cv.positive_time_period_milliseconds,
        }), cv.has_at_least_one_key(CONF_STATE, CONF_BRIGHTNESS, CONF_RED, CONF_GREEN, CONF_BLUE,
                                    CONF_WHITE))], vol.Length(min=2)),
    }),
    vol.Optional(CONF_FLICKER): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FlickerLightEffect),
        vol.Optional(CONF_NAME, default="Flicker"): cv.string,
        vol.Optional(CONF_ALPHA): cv.percentage,
        vol.Optional(CONF_INTENSITY): cv.percentage,
    }),
    vol.Optional(CONF_FASTLED_LAMBDA): vol.Schema({
        vol.Required(CONF_NAME): cv.string,
        vol.Required(CONF_LAMBDA): cv.lambda_,
        vol.Optional(CONF_UPDATE_INTERVAL, default='0ms'): cv.positive_time_period_milliseconds,
    }),
    vol.Optional(CONF_FASTLED_RAINBOW): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDRainbowLightEffect),
        vol.Optional(CONF_NAME, default="Rainbow"): cv.string,
        vol.Optional(CONF_SPEED): cv.uint32_t,
        vol.Optional(CONF_WIDTH): cv.uint32_t,
    }),
    vol.Optional(CONF_FASTLED_COLOR_WIPE): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDColorWipeEffect),
        vol.Optional(CONF_NAME, default="Color Wipe"): cv.string,
        vol.Optional(CONF_COLORS): vol.All(cv.ensure_list, [vol.Schema({
            vol.Optional(CONF_RED, default=1.0): cv.percentage,
            vol.Optional(CONF_GREEN, default=1.0): cv.percentage,
            vol.Optional(CONF_BLUE, default=1.0): cv.percentage,
            vol.Optional(CONF_RANDOM, default=False): cv.boolean,
            vol.Required(CONF_NUM_LEDS): vol.All(cv.uint32_t, vol.Range(min=1)),
        })]),
        vol.Optional(CONF_ADD_LED_INTERVAL): cv.positive_time_period_milliseconds,
        vol.Optional(CONF_REVERSE): cv.boolean,
    }),
    vol.Optional(CONF_FASTLED_SCAN): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDScanEffect),
        vol.Optional(CONF_NAME, default="Scan"): cv.string,
        vol.Optional(CONF_MOVE_INTERVAL): cv.positive_time_period_milliseconds,
    }),
    vol.Optional(CONF_FASTLED_TWINKLE): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDTwinkleEffect),
        vol.Optional(CONF_NAME, default="Twinkle"): cv.string,
        vol.Optional(CONF_TWINKLE_PROBABILITY): cv.percentage,
        vol.Optional(CONF_PROGRESS_INTERVAL): cv.positive_time_period_milliseconds,
    }),
    vol.Optional(CONF_FASTLED_RANDOM_TWINKLE): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDRandomTwinkleEffect),
        vol.Optional(CONF_NAME, default="Random Twinkle"): cv.string,
        vol.Optional(CONF_TWINKLE_PROBABILITY): cv.percentage,
        vol.Optional(CONF_PROGRESS_INTERVAL): cv.positive_time_period_milliseconds,
    }),
    vol.Optional(CONF_FASTLED_FIREWORKS): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDFireworksEffect),
        vol.Optional(CONF_NAME, default="Fireworks"): cv.string,
        vol.Optional(CONF_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
        vol.Optional(CONF_SPARK_PROBABILITY): cv.percentage,
        vol.Optional(CONF_USE_RANDOM_COLOR): cv.boolean,
        vol.Optional(CONF_FADE_OUT_RATE): cv.uint8_t,
    }),
    vol.Optional(CONF_FASTLED_FLICKER): vol.Schema({
        cv.GenerateID(CONF_EFFECT_ID): cv.declare_variable_id(FastLEDFlickerEffect),
        vol.Optional(CONF_NAME, default="FastLED Flicker"): cv.string,
        vol.Optional(CONF_UPDATE_INTERVAL): cv.positive_time_period_milliseconds,
        vol.Optional(CONF_INTENSITY): cv.percentage,
    }),
})


def validate_effects(allowed_effects):
    def validator(value):
        value = cv.ensure_list(value)
        names = set()
        ret = []
        for i, effect in enumerate(value):
            if not isinstance(effect, dict):
                raise vol.Invalid("Each effect must be a dictionary, not {}".format(type(value)))
            if len(effect) > 1:
                raise vol.Invalid("Each entry in the 'effects:' option must be a single effect.")
            if not effect:
                raise vol.Invalid("Found no effect for the {}th entry in 'effects:'!".format(i))
            key = next(iter(effect.keys()))
            if key not in allowed_effects:
                raise vol.Invalid("The effect '{}' does not exist or is not allowed for this "
                                  "light type".format(key))
            effect[key] = effect[key] or {}
            conf = EFFECTS_SCHEMA(effect)
            name = conf[key][CONF_NAME]
            if name in names:
                raise vol.Invalid(u"Found the effect name '{}' twice. All effects must have "
                                  u"unique names".format(name))
            names.add(name)
            ret.append(conf)
        return ret

    return validator


LIGHT_SCHEMA = cv.MQTT_COMMAND_COMPONENT_SCHEMA.extend({
    cv.GenerateID(): cv.declare_variable_id(LightState),
    cv.GenerateID(CONF_MQTT_ID): cv.declare_variable_id(MQTTJSONLightComponent),
})

LIGHT_PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(LIGHT_SCHEMA.schema)


def build_effect(full_config):
    key, config = next(iter(full_config.items()))
    if key == CONF_LAMBDA:
        lambda_ = None
        for lambda_ in process_lambda(config[CONF_LAMBDA], []):
            yield None
        yield LambdaLightEffect.new(config[CONF_NAME], lambda_, config[CONF_UPDATE_INTERVAL])
    elif key == CONF_RANDOM:
        rhs = RandomLightEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_TRANSITION_LENGTH in config:
            add(effect.set_transition_length(config[CONF_TRANSITION_LENGTH]))
        if CONF_UPDATE_INTERVAL in config:
            add(effect.set_update_interval(config[CONF_UPDATE_INTERVAL]))
        yield effect
    elif key == CONF_STROBE:
        rhs = StrobeLightEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        colors = []
        for color in config.get(CONF_COLORS, []):
            colors.append(StructInitializer(
                StrobeLightEffectColor,
                ('color', LightColorValues(color[CONF_STATE], color[CONF_BRIGHTNESS],
                                           color[CONF_RED], color[CONF_GREEN], color[CONF_BLUE],
                                           color[CONF_WHITE])),
                ('duration', color[CONF_DURATION]),
            ))
        if colors:
            add(effect.set_colors(ArrayInitializer(*colors)))
        yield effect
    elif key == CONF_FLICKER:
        rhs = FlickerLightEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_ALPHA in config:
            add(effect.set_alpha(config[CONF_ALPHA]))
        if CONF_INTENSITY in config:
            add(effect.set_intensity(config[CONF_INTENSITY]))
        yield effect
    elif key == CONF_FASTLED_LAMBDA:
        lambda_ = None
        args = [(RawExpression('FastLEDLightOutputComponent &'), 'it')]
        for lambda_ in process_lambda(config[CONF_LAMBDA], args):
            yield None
        yield FastLEDLambdaLightEffect.new(config[CONF_NAME], lambda_, config[CONF_UPDATE_INTERVAL])
    elif key == CONF_FASTLED_RAINBOW:
        rhs = FastLEDRainbowLightEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_SPEED in config:
            add(effect.set_speed(config[CONF_SPEED]))
        if CONF_WIDTH in config:
            add(effect.set_width(config[CONF_WIDTH]))
        yield effect
    elif key == CONF_FASTLED_COLOR_WIPE:
        rhs = FastLEDColorWipeEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_ADD_LED_INTERVAL in config:
            add(effect.set_add_led_interval(config[CONF_ADD_LED_INTERVAL]))
        if CONF_REVERSE in config:
            add(effect.set_reverse(config[CONF_REVERSE]))
        colors = []
        for color in config.get(CONF_COLORS, []):
            colors.append(StructInitializer(
                FastLEDColorWipeEffectColor,
                ('r', color[CONF_RED]),
                ('g', color[CONF_GREEN]),
                ('b', color[CONF_BLUE]),
                ('random', color[CONF_RANDOM]),
                ('num_leds', color[CONF_NUM_LEDS]),
            ))
        if colors:
            add(effect.set_colors(ArrayInitializer(*colors)))
        yield effect
    elif key == CONF_FASTLED_SCAN:
        rhs = FastLEDScanEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_MOVE_INTERVAL in config:
            add(effect.set_move_interval(config[CONF_MOVE_INTERVAL]))
        yield effect
    elif key == CONF_FASTLED_TWINKLE:
        rhs = FastLEDTwinkleEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_TWINKLE_PROBABILITY in config:
            add(effect.set_twinkle_probability(config[CONF_TWINKLE_PROBABILITY]))
        if CONF_PROGRESS_INTERVAL in config:
            add(effect.set_progress_interval(config[CONF_PROGRESS_INTERVAL]))
        yield effect
    elif key == CONF_FASTLED_RANDOM_TWINKLE:
        rhs = FastLEDRandomTwinkleEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_TWINKLE_PROBABILITY in config:
            add(effect.set_twinkle_probability(config[CONF_TWINKLE_PROBABILITY]))
        if CONF_PROGRESS_INTERVAL in config:
            add(effect.set_progress_interval(config[CONF_PROGRESS_INTERVAL]))
        yield effect
    elif key == CONF_FASTLED_FIREWORKS:
        rhs = FastLEDFireworksEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_UPDATE_INTERVAL in config:
            add(effect.set_update_interval(config[CONF_UPDATE_INTERVAL]))
        if CONF_SPARK_PROBABILITY in config:
            add(effect.set_spark_probability(config[CONF_SPARK_PROBABILITY]))
        if CONF_USE_RANDOM_COLOR in config:
            add(effect.set_spark_probability(config[CONF_USE_RANDOM_COLOR]))
        if CONF_FADE_OUT_RATE in config:
            add(effect.set_spark_probability(config[CONF_FADE_OUT_RATE]))
        yield effect
    elif key == CONF_FASTLED_FLICKER:
        rhs = FastLEDFlickerEffect.new(config[CONF_NAME])
        effect = Pvariable(config[CONF_EFFECT_ID], rhs)
        if CONF_UPDATE_INTERVAL in config:
            add(effect.set_update_interval(config[CONF_UPDATE_INTERVAL]))
        if CONF_INTENSITY in config:
            add(effect.set_intensity(config[CONF_INTENSITY]))
        yield effect
    else:
        raise NotImplementedError("Effect {} not implemented".format(next(config.keys())))


def setup_light_core_(light_var, mqtt_var, config):
    if CONF_INTERNAL in config:
        add(light_var.set_internal(config[CONF_INTERNAL]))
    if CONF_DEFAULT_TRANSITION_LENGTH in config:
        add(light_var.set_default_transition_length(config[CONF_DEFAULT_TRANSITION_LENGTH]))
    if CONF_GAMMA_CORRECT in config:
        add(light_var.set_gamma_correct(config[CONF_GAMMA_CORRECT]))
    effects = []
    for conf in config.get(CONF_EFFECTS, []):
        for effect in build_effect(conf):
            yield
        effects.append(effect)
    if effects:
        add(light_var.add_effects(ArrayInitializer(*effects)))

    setup_mqtt_component(mqtt_var, config)


def setup_light(light_obj, mqtt_obj, config):
    light_var = Pvariable(config[CONF_ID], light_obj, has_side_effects=False)
    mqtt_var = Pvariable(config[CONF_MQTT_ID], mqtt_obj, has_side_effects=False)
    add_job(setup_light_core_, light_var, mqtt_var, config)


BUILD_FLAGS = '-DUSE_LIGHT'

CONF_LIGHT_TOGGLE = 'light.toggle'
LIGHT_TOGGLE_ACTION_SCHEMA = maybe_simple_id({
    vol.Required(CONF_ID): cv.use_variable_id(LightState),
    vol.Optional(CONF_TRANSITION_LENGTH): cv.templatable(cv.positive_time_period_milliseconds),
})


@ACTION_REGISTRY.register(CONF_LIGHT_TOGGLE, LIGHT_TOGGLE_ACTION_SCHEMA)
def light_toggle_to_code(config, action_id, arg_type):
    template_arg = TemplateArguments(arg_type)
    for var in get_variable(config[CONF_ID]):
        yield None
    rhs = var.make_toggle_action(template_arg)
    type = ToggleAction.template(template_arg)
    action = Pvariable(action_id, rhs, type=type)
    if CONF_TRANSITION_LENGTH in config:
        for template_ in templatable(config[CONF_TRANSITION_LENGTH], arg_type, uint32):
            yield None
        add(action.set_transition_length(template_))
    yield action


CONF_LIGHT_TURN_OFF = 'light.turn_off'
LIGHT_TURN_OFF_ACTION_SCHEMA = maybe_simple_id({
    vol.Required(CONF_ID): cv.use_variable_id(LightState),
    vol.Optional(CONF_TRANSITION_LENGTH): cv.templatable(cv.positive_time_period_milliseconds),
})


@ACTION_REGISTRY.register(CONF_LIGHT_TURN_OFF, LIGHT_TURN_OFF_ACTION_SCHEMA)
def light_turn_off_to_code(config, action_id, arg_type):
    template_arg = TemplateArguments(arg_type)
    for var in get_variable(config[CONF_ID]):
        yield None
    rhs = var.make_turn_off_action(template_arg)
    type = TurnOffAction.template(template_arg)
    action = Pvariable(action_id, rhs, type=type)
    if CONF_TRANSITION_LENGTH in config:
        for template_ in templatable(config[CONF_TRANSITION_LENGTH], arg_type, uint32):
            yield None
        add(action.set_transition_length(template_))
    yield action


CONF_LIGHT_TURN_ON = 'light.turn_on'
LIGHT_TURN_ON_ACTION_SCHEMA = maybe_simple_id({
    vol.Required(CONF_ID): cv.use_variable_id(LightState),
    vol.Exclusive(CONF_TRANSITION_LENGTH, 'transformer'):
        cv.templatable(cv.positive_time_period_milliseconds),
    vol.Exclusive(CONF_FLASH_LENGTH, 'transformer'):
        cv.templatable(cv.positive_time_period_milliseconds),
    vol.Optional(CONF_BRIGHTNESS): cv.templatable(cv.percentage),
    vol.Optional(CONF_RED): cv.templatable(cv.percentage),
    vol.Optional(CONF_GREEN): cv.templatable(cv.percentage),
    vol.Optional(CONF_BLUE): cv.templatable(cv.percentage),
    vol.Optional(CONF_WHITE): cv.templatable(cv.percentage),
    vol.Optional(CONF_COLOR_TEMPERATURE): cv.templatable(cv.positive_float),
    vol.Optional(CONF_EFFECT): cv.templatable(cv.string),
})


@ACTION_REGISTRY.register(CONF_LIGHT_TURN_ON, LIGHT_TURN_ON_ACTION_SCHEMA)
def light_turn_on_to_code(config, action_id, arg_type):
    template_arg = TemplateArguments(arg_type)
    for var in get_variable(config[CONF_ID]):
        yield None
    rhs = var.make_turn_on_action(template_arg)
    type = TurnOnAction.template(template_arg)
    action = Pvariable(action_id, rhs, type=type)
    if CONF_TRANSITION_LENGTH in config:
        for template_ in templatable(config[CONF_TRANSITION_LENGTH], arg_type, uint32):
            yield None
        add(action.set_transition_length(template_))
    if CONF_FLASH_LENGTH in config:
        for template_ in templatable(config[CONF_FLASH_LENGTH], arg_type, uint32):
            yield None
        add(action.set_flash_length(template_))
    if CONF_BRIGHTNESS in config:
        for template_ in templatable(config[CONF_BRIGHTNESS], arg_type, float_):
            yield None
        add(action.set_brightness(template_))
    if CONF_RED in config:
        for template_ in templatable(config[CONF_RED], arg_type, float_):
            yield None
        add(action.set_red(template_))
    if CONF_GREEN in config:
        for template_ in templatable(config[CONF_GREEN], arg_type, float_):
            yield None
        add(action.set_green(template_))
    if CONF_BLUE in config:
        for template_ in templatable(config[CONF_BLUE], arg_type, float_):
            yield None
        add(action.set_blue(template_))
    if CONF_WHITE in config:
        for template_ in templatable(config[CONF_WHITE], arg_type, float_):
            yield None
        add(action.set_white(template_))
    if CONF_COLOR_TEMPERATURE in config:
        for template_ in templatable(config[CONF_COLOR_TEMPERATURE], arg_type, float_):
            yield None
        add(action.set_color_temperature(template_))
    if CONF_EFFECT in config:
        for template_ in templatable(config[CONF_EFFECT], arg_type, std_string):
            yield None
        add(action.set_effect(template_))
    yield action


def core_to_hass_config(data, config, brightness=True, rgb=True, color_temp=True,
                        white_value=True):
    ret = mqtt.build_hass_config(data, 'light', config, include_state=True, include_command=True,
                                 platform='mqtt_json')
    if ret is None:
        return None
    if brightness:
        ret['brightness'] = True
    if rgb:
        ret['rgb'] = True
    if color_temp:
        ret['color_temp'] = True
    if white_value:
        ret['white_value'] = True
    for effect in config.get(CONF_EFFECTS, []):
        ret["effect"] = True
        effects = ret.setdefault("effect_list", [])
        effects.append(next(x for x in effect.values())[CONF_NAME])
    return ret
