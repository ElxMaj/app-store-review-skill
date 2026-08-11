#!/usr/bin/env ruby

require "json"
require "yaml"


def collect_uses(node, path, entries)
  if node.is_a?(Psych::Nodes::Mapping)
    node.children.each_slice(2) do |key, value|
      if key.is_a?(Psych::Nodes::Scalar) && key.value == "uses"
        unless value.is_a?(Psych::Nodes::Scalar)
          raise "#{path}:#{value.start_line + 1}: uses value must be a scalar"
        end
        entries << {
          "path" => path,
          "line" => value.start_line + 1,
          "value" => value.value,
        }
      end
      collect_uses(key, path, entries)
      collect_uses(value, path, entries)
    end
    return
  end

  return unless node.respond_to?(:children) && node.children

  node.children.each { |child| collect_uses(child, path, entries) }
end


begin
  entries = []
  ARGV.each do |path|
    document = YAML.parse_file(path)
    raise "#{path}: YAML document is empty" if document.nil?

    collect_uses(document, path, entries)
  end
  puts JSON.generate(entries)
rescue StandardError => error
  warn error.message
  exit 1
end
