shader_type spatial;
render_mode cull_disabled, specular_schlick_ggx;
// Cheap animated water: two scrolling normal-ish ripples, depth-free colour blend, fresnel sky reflection, soft glints.
uniform vec4 deep_color : source_color = vec4(0.1, 0.25, 0.35, 1.0);
uniform vec4 shallow_color : source_color = vec4(0.3, 0.5, 0.55, 1.0);
uniform vec4 sky_color : source_color = vec4(0.6, 0.7, 0.8, 1.0);
uniform float wave_strength = 0.25;

float hash(vec2 p) { return fract(sin(dot(p, vec2(127.1, 311.7))) * 43758.5453); }
float noise(vec2 p) {
	vec2 i = floor(p);
	vec2 f = fract(p);
	f = f * f * (3.0 - 2.0 * f);
	return mix(mix(hash(i), hash(i + vec2(1, 0)), f.x), mix(hash(i + vec2(0, 1)), hash(i + vec2(1, 1)), f.x), f.y);
}
float height(vec2 p, float t) {
	return noise(p * 0.35 + vec2(t * 0.08, t * 0.05)) * 0.6 + noise(p * 0.9 - vec2(t * 0.12, -t * 0.09)) * 0.3 + noise(p * 2.3 + vec2(t * 0.2)) * 0.1;
}

void fragment() {
	vec3 wp = (INV_VIEW_MATRIX * vec4(VERTEX, 1.0)).xyz;
	float t = TIME;
	float e = 0.08;
	float h = height(wp.xz, t);
	float hx = height(wp.xz + vec2(e, 0.0), t);
	float hz = height(wp.xz + vec2(0.0, e), t);
	vec3 n = normalize(vec3((h - hx) * wave_strength * 6.0, 1.0, (h - hz) * wave_strength * 6.0));
	NORMAL = (VIEW_MATRIX * vec4(n, 0.0)).xyz;
	float fres = pow(1.0 - clamp(dot(normalize(NORMAL), normalize(VIEW)), 0.0, 1.0), 3.0);
	vec3 base = mix(deep_color.rgb, shallow_color.rgb, h);
	ALBEDO = mix(base * 0.85, sky_color.rgb, fres * 0.5);
	ROUGHNESS = 0.12;
	SPECULAR = 0.8;
	METALLIC = 0.0;
}
